from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core.entities import User
from core.services import (
    BudgetService,
    CategoryService,
    EmojiService,
    PasswordService,
    TokenService,
    TransactionService,
    UserService,
)
from core.use_cases.auth.authenticate import AuthenticationUseCase
from repos import (
    FileBudgetService,
    FileCategoryService,
    FileTokenService,
    FileTransactionService,
    FileUserService,
)
from services import EmojiPackageService, PasswordBcryptService

header_scheme = APIKeyHeader(
    name="Authorization", auto_error=False, description='Token in format: "Authorization": "{TOKEN}"'
)


def password_service_factory() -> PasswordService:
    return PasswordBcryptService()


def emoji_service_factory() -> EmojiService:
    return EmojiPackageService()


def token_service_factory() -> TokenService:
    return FileTokenService()


def user_service_factory() -> UserService:
    return FileUserService()


def budget_service_factory() -> BudgetService:
    return FileBudgetService()


def category_service_factory() -> CategoryService:
    return FileCategoryService()


def transaction_service_factory() -> TransactionService:
    return FileTransactionService()


async def authentication_user(
    token: Annotated[str | None, Depends(header_scheme)],
    user_service: Annotated[UserService, Depends(user_service_factory)],
    token_service: Annotated[TokenService, Depends(token_service_factory)],
) -> User:
    use_case = AuthenticationUseCase(token_service=token_service, user_service=user_service)
    return await use_case.authenticate(token=token)
