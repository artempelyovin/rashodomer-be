from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core.entities import User
from core.repos import BudgetRepository, CategoryRepository, ExpenseRepository, IncomeRepository, UserRepository
from core.services import (
    EmojiService,
    PasswordService, TokenService,
)
from core.use_cases.auth.authenticate import AuthenticationUseCase
from repos import (
    FileBudgetRepository,
    FileCategoryRepository,
    FileExpenseRepository,
    FileIncomeRepository,
    FileTokenService,
    FileUserRepository,
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


def user_service_factory() -> UserRepository:
    return FileUserRepository()


def budget_service_factory() -> BudgetRepository:
    return FileBudgetRepository()


def category_service_factory() -> CategoryRepository:
    return FileCategoryRepository()


def expense_service_factory() -> ExpenseRepository:
    return FileExpenseRepository()


def income_service_factory() -> IncomeRepository:
    return FileIncomeRepository()


async def authentication_user(
    token: Annotated[str | None, Depends(header_scheme)],
    user_service: Annotated[UserRepository, Depends(user_service_factory)],
    token_service: Annotated[TokenService, Depends(token_service_factory)],
) -> User:
    use_case = AuthenticationUseCase(token_service=token_service, user_service=user_service)
    return await use_case.authenticate(token=token)
