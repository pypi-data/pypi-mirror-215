from typing import Any, cast

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_users import BaseUserManager, InvalidPasswordException
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    Strategy,
)
from fastapi_users.exceptions import UserAlreadyExists, UserNotExists
from fastapi_users.manager import UUIDIDMixin
from fastapi_users.password import PasswordHelperProtocol
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTable,
    SQLAlchemyUserDatabase,
)
from furl import furl
from jwcrypto import jwk
from pydantic import UUID4, ValidationError, create_model
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from fief.crypto.access_token import InvalidAccessToken, read_access_token
from fief.crypto.password import password_helper
from fief.db import AsyncSession
from fief.dependencies.current_workspace import (
    get_current_workspace,
    get_current_workspace_session,
)
from fief.dependencies.logger import get_audit_logger
from fief.dependencies.pagination import (
    GetPaginatedObjects,
    Ordering,
    OrderingGetter,
    PaginatedObjects,
    Pagination,
    get_paginated_objects_getter,
    get_pagination,
)
from fief.dependencies.request import get_request_json
from fief.dependencies.tasks import get_send_task
from fief.dependencies.tenant import (
    get_current_tenant,
    get_tenant_from_create_user_internal,
)
from fief.dependencies.user_field import (
    get_admin_user_create_internal_model,
    get_admin_user_update_model,
    get_user_update_model,
)
from fief.dependencies.webhooks import TriggerWebhooks, get_trigger_webhooks
from fief.dependencies.workspace_repositories import get_workspace_repository
from fief.logger import AuditLogger
from fief.models import (
    AuditLogMessage,
    OAuthAccount,
    Tenant,
    User,
    UserField,
    UserFieldValue,
    UserPermission,
    UserRole,
    Workspace,
)
from fief.repositories import (
    OAuthAccountRepository,
    UserPermissionRepository,
    UserRepository,
    UserRoleRepository,
)
from fief.schemas.user import UF, UserCreate, UserCreateInternal, UserRead, UserUpdate
from fief.services.password import PasswordValidation
from fief.services.webhooks.models import (
    UserCreated,
    UserForgotPasswordRequested,
    UserPasswordReset,
    UserUpdated,
)
from fief.settings import settings
from fief.tasks import SendTask, on_after_forgot_password, on_after_register


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
    reset_password_token_secret = settings.secret.get_secret_value()
    verification_token_secret = settings.secret.get_secret_value()

    def __init__(
        self,
        user_db: SQLAlchemyUserDatabase[User, UUID4],
        password_helper: PasswordHelperProtocol,
        workspace: Workspace,
        tenant: Tenant,
        send_task: SendTask,
        audit_logger: AuditLogger,
        trigger_webhooks: TriggerWebhooks,
    ):
        super().__init__(user_db, password_helper)
        self.workspace = workspace
        self.tenant = tenant
        self.send_task = send_task
        self.audit_logger = audit_logger
        self.trigger_webhooks = trigger_webhooks

    async def validate_password(  # type: ignore
        self, password: str, user: UserCreate | User
    ) -> None:
        password_validation = PasswordValidation.validate(password)
        if not password_validation.valid:
            raise InvalidPasswordException(password_validation.messages)

    async def create_with_fields(
        self,
        user_create: UserCreate[UF],
        *,
        user_fields: list[UserField],
        safe: bool = False,
        request: Request | None = None,
    ) -> User:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        user = await self.user_db.create(user_dict)
        await self.user_db.session.refresh(user)  # type: ignore

        for user_field in user_fields:
            user_field_value = UserFieldValue(user_field=user_field)
            try:
                value = user_create.fields.get_value(user_field.slug)
                if value is not None:
                    user_field_value.value = value
                    user.user_field_values.append(user_field_value)
            except AttributeError:
                default = user_field.get_default()
                if default is not None:
                    user_field_value.value = default
                    user.user_field_values.append(user_field_value)

        user = await self.user_db.update(user, {})

        await self.on_after_register(user, request)

        return user

    async def update_with_fields(
        self,
        user_update: UserUpdate[UF],
        user: User,
        *,
        user_fields: list[UserField],
        safe: bool = False,
        request: Request | None = None,
    ) -> User:
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        user = await self._update(user, updated_user_data)

        if user_update.fields is not None:
            for user_field in user_fields:
                existing_user_field_value = user.get_user_field_value(user_field)
                # Update existing value
                if existing_user_field_value is not None:
                    try:
                        value = user_update.fields.get_value(user_field.slug)
                        if value is not None:
                            existing_user_field_value.value = value
                    except AttributeError:
                        pass
                # Create new value
                else:
                    user_field_value = UserFieldValue(user_field=user_field)
                    try:
                        value = user_update.fields.get_value(user_field.slug)
                        if value is not None:
                            user_field_value.value = value
                            user.user_field_values.append(user_field_value)
                    except AttributeError:
                        default = user_field.get_default()
                        if default is not None:
                            user_field_value.value = default
                            user.user_field_values.append(user_field_value)

            user = await self.user_db.update(user, {})

        await self.on_after_update(user, updated_user_data, request)

        return user

    async def on_after_register(self, user: User, request: Request | None = None):
        await self.user_db.session.refresh(user)  # type: ignore
        self.audit_logger(AuditLogMessage.USER_REGISTERED, subject_user_id=user.id)
        self.trigger_webhooks(UserCreated, user, UserRead)
        self.send_task(on_after_register, str(user.id), str(self.workspace.id))

    async def on_after_update(
        self, user: User, update_dict: dict[str, Any], request: Request | None = None
    ):
        self.audit_logger(AuditLogMessage.USER_UPDATED, subject_user_id=user.id)
        self.trigger_webhooks(UserUpdated, user, UserRead)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        self.audit_logger(
            AuditLogMessage.USER_FORGOT_PASSWORD_REQUESTED, subject_user_id=user.id
        )
        self.trigger_webhooks(UserForgotPasswordRequested, user, UserRead)

        reset_url = furl(self.tenant.url_for(cast(Request, request), "reset:reset"))
        reset_url.add(query_params={"token": token})
        self.send_task(
            on_after_forgot_password,
            str(user.id),
            str(self.workspace.id),
            reset_url.url,
        )

    async def on_after_reset_password(
        self, user: User, request: Request | None = None
    ) -> None:
        self.audit_logger(AuditLogMessage.USER_PASSWORD_RESET, subject_user_id=user.id)
        self.trigger_webhooks(UserPasswordReset, user, UserRead)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


class SQLAlchemyUserTenantDatabase(SQLAlchemyUserDatabase[User, UUID4]):
    def __init__(
        self,
        session: AsyncSession,
        tenant: Tenant,
        user_table: type[User],
        oauth_account_table: type[SQLAlchemyBaseOAuthAccountTable] | None = None,
    ):
        super().__init__(session, user_table, oauth_account_table=oauth_account_table)
        self.tenant = tenant

    async def _get_user(self, statement: Select) -> User | None:
        statement = statement.where(User.tenant_id == self.tenant.id)
        return await super()._get_user(statement)


class JWTAccessTokenStrategy(Strategy[User, UUID4]):
    def __init__(self, key: jwk.JWK):
        self.key = key

    async def read_token(
        self, token: str | None, user_manager: BaseUserManager[User, UUID4]
    ) -> User | None:
        if token is None:
            return None

        try:
            user_id = read_access_token(self.key, token)
            user = await user_manager.get(user_id)
        except InvalidAccessToken:
            return None
        except UserNotExists:
            return None
        else:
            return user

    async def write_token(self, user: User) -> str:
        raise NotImplementedError()

    async def destroy_token(self, token: str, user: User) -> None:
        raise NotImplementedError()


async def get_jwt_access_token_strategy(
    tenant: Tenant = Depends(get_current_tenant),
) -> JWTAccessTokenStrategy:
    return JWTAccessTokenStrategy(tenant.get_sign_jwk())


async def get_user_db(
    session: AsyncSession = Depends(get_current_workspace_session),
    tenant: Tenant = Depends(get_current_tenant),
) -> SQLAlchemyUserDatabase[User, UUID4]:
    return SQLAlchemyUserTenantDatabase(session, tenant, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[User, UUID4] = Depends(get_user_db),
    tenant: Tenant = Depends(get_current_tenant),
    workspace: Workspace = Depends(get_current_workspace),
    send_task: SendTask = Depends(get_send_task),
    audit_logger: AuditLogger = Depends(get_audit_logger),
    trigger_webhooks: TriggerWebhooks = Depends(get_trigger_webhooks),
):
    return UserManager(
        user_db,
        password_helper,
        workspace,
        tenant,
        send_task,
        audit_logger,
        trigger_webhooks,
    )


async def get_user_db_from_create_user_internal(
    session: AsyncSession = Depends(get_current_workspace_session),
    tenant: Tenant = Depends(get_tenant_from_create_user_internal),
) -> SQLAlchemyUserDatabase[User, UUID4]:
    return SQLAlchemyUserTenantDatabase(session, tenant, User)


async def get_user_manager_from_create_user_internal(
    user_db: SQLAlchemyUserDatabase[User, UUID4] = Depends(
        get_user_db_from_create_user_internal
    ),
    tenant: Tenant = Depends(get_tenant_from_create_user_internal),
    workspace: Workspace = Depends(get_current_workspace),
    send_task: SendTask = Depends(get_send_task),
    audit_logger: AuditLogger = Depends(get_audit_logger),
    trigger_webhooks: TriggerWebhooks = Depends(get_trigger_webhooks),
):
    return UserManager(
        user_db,
        password_helper,
        workspace,
        tenant,
        send_task,
        audit_logger,
        trigger_webhooks,
    )


class AuthorizationCodeBearerTransport(BearerTransport):
    scheme: OAuth2AuthorizationCodeBearer  # type: ignore

    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        refreshUrl: str,
        scopes: dict[str, str],
    ):
        self.scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl, tokenUrl, refreshUrl, scopes=scopes
        )


authentication_backend = AuthenticationBackend[User, UUID4](
    "jwt_access_token",
    AuthorizationCodeBearerTransport(
        "/authorize", "/api/token", "/api/token", {"openid": "openid"}
    ),
    get_jwt_access_token_strategy,
)


async def get_paginated_users(
    query: str | None = Query(None),
    email: str | None = Query(None),
    tenant: UUID4 | None = Query(None),
    pagination: Pagination = Depends(get_pagination),
    ordering: Ordering = Depends(OrderingGetter()),
    repository: UserRepository = Depends(get_workspace_repository(UserRepository)),
    get_paginated_objects: GetPaginatedObjects[User] = Depends(
        get_paginated_objects_getter
    ),
) -> PaginatedObjects[User]:
    statement = select(User).options(joinedload(User.tenant))
    if query is not None:
        statement = statement.where(User.email.ilike(f"%{query}%"))  # type: ignore
    if email is not None:
        statement = statement.where(User.email == email)  # type: ignore
    if tenant is not None:
        statement = statement.where(User.tenant_id == tenant)
    return await get_paginated_objects(statement, pagination, ordering, repository)


async def get_user_by_id_or_404(
    id: UUID4,
    repository: UserRepository = Depends(get_workspace_repository(UserRepository)),
) -> User:
    user = await repository.get_by_id(id, (joinedload(User.tenant),))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


async def get_paginated_user_permissions(
    pagination: Pagination = Depends(get_pagination),
    ordering: Ordering = Depends(OrderingGetter()),
    user: User = Depends(get_user_by_id_or_404),
    user_permission_repository: UserPermissionRepository = Depends(
        get_workspace_repository(UserPermissionRepository)
    ),
    get_paginated_objects: GetPaginatedObjects[UserPermission] = Depends(
        get_paginated_objects_getter
    ),
) -> PaginatedObjects[UserPermission]:
    statement = user_permission_repository.get_by_user_statement(user.id)
    return await get_paginated_objects(
        statement, pagination, ordering, user_permission_repository
    )


async def get_user_permissions(
    user: User = Depends(get_user_by_id_or_404),
    user_permission_repository: UserPermissionRepository = Depends(
        get_workspace_repository(UserPermissionRepository)
    ),
) -> list[UserPermission]:
    statement = user_permission_repository.get_by_user_statement(user.id)
    return await user_permission_repository.list(statement)


async def get_paginated_user_roles(
    pagination: Pagination = Depends(get_pagination),
    ordering: Ordering = Depends(OrderingGetter()),
    user: User = Depends(get_user_by_id_or_404),
    user_role_repository: UserRoleRepository = Depends(
        get_workspace_repository(UserRoleRepository)
    ),
    get_paginated_objects: GetPaginatedObjects[UserRole] = Depends(
        get_paginated_objects_getter
    ),
) -> PaginatedObjects[UserRole]:
    statement = user_role_repository.get_by_user_statement(user.id)
    return await get_paginated_objects(
        statement, pagination, ordering, user_role_repository
    )


async def get_user_roles(
    user: User = Depends(get_user_by_id_or_404),
    user_role_repository: UserRoleRepository = Depends(
        get_workspace_repository(UserRoleRepository)
    ),
) -> list[UserRole]:
    statement = user_role_repository.get_by_user_statement(user.id)
    return await user_role_repository.list(statement)


async def get_paginated_user_oauth_accounts(
    pagination: Pagination = Depends(get_pagination),
    ordering: Ordering = Depends(OrderingGetter()),
    user: User = Depends(get_user_by_id_or_404),
    oauth_account_repository: OAuthAccountRepository = Depends(
        get_workspace_repository(OAuthAccountRepository)
    ),
    get_paginated_objects: GetPaginatedObjects[OAuthAccount] = Depends(
        get_paginated_objects_getter
    ),
) -> PaginatedObjects[OAuthAccount]:
    statement = oauth_account_repository.get_by_user_statement(user.id)
    return await get_paginated_objects(
        statement, pagination, ordering, oauth_account_repository
    )


async def get_user_oauth_accounts(
    user: User = Depends(get_user_by_id_or_404),
    oauth_account_repository: OAuthAccountRepository = Depends(
        get_workspace_repository(OAuthAccountRepository)
    ),
) -> list[OAuthAccount]:
    statement = oauth_account_repository.get_by_user_statement(user.id)
    return await oauth_account_repository.list(statement)


async def get_user_db_from_user(
    user: User = Depends(get_user_by_id_or_404),
    session: AsyncSession = Depends(get_current_workspace_session),
) -> SQLAlchemyUserDatabase[User, UUID4]:
    return SQLAlchemyUserTenantDatabase(session, user.tenant, User)


async def get_user_manager_from_user(
    user: User = Depends(get_user_by_id_or_404),
    user_db: SQLAlchemyUserDatabase[User, UUID4] = Depends(get_user_db_from_user),
    workspace: Workspace = Depends(get_current_workspace),
    send_task: SendTask = Depends(get_send_task),
    audit_logger: AuditLogger = Depends(get_audit_logger),
    trigger_webhooks: TriggerWebhooks = Depends(get_trigger_webhooks),
):
    return UserManager(
        user_db,
        password_helper,
        workspace,
        user.tenant,
        send_task,
        audit_logger,
        trigger_webhooks,
    )


async def get_user_create_internal(
    json: dict[str, Any] = Depends(get_request_json),
    user_create_internal_model: type[UserCreateInternal[UF]] = Depends(
        get_admin_user_create_internal_model
    ),
) -> UserCreateInternal[UF]:
    body_model = create_model(
        "UserCreateInternalBody",
        body=(user_create_internal_model, ...),
    )
    try:
        validated_user_create_internal = body_model(body=json)
    except ValidationError as e:
        raise RequestValidationError(e.raw_errors) from e
    else:
        return validated_user_create_internal.body  # type: ignore


async def get_user_update(
    json: dict[str, Any] = Depends(get_request_json),
    user_update_model: type[UserUpdate[UF]] = Depends(get_user_update_model),
) -> UserUpdate[UF]:
    body_model = create_model(
        "UserUpdateBody",
        body=(user_update_model, ...),
    )
    try:
        validated_user_update = body_model(body=json)
    except ValidationError as e:
        raise RequestValidationError(e.raw_errors) from e
    else:
        return validated_user_update.body  # type: ignore


async def get_admin_user_update(
    json: dict[str, Any] = Depends(get_request_json),
    user_update_model: type[UserUpdate[UF]] = Depends(get_admin_user_update_model),
) -> UserUpdate[UF]:
    body_model = create_model(
        "UserUpdateBody",
        body=(user_update_model, ...),
    )
    try:
        validated_user_update = body_model(body=json)
    except ValidationError as e:
        raise RequestValidationError(e.raw_errors) from e
    else:
        return validated_user_update.body  # type: ignore
