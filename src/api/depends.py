from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core.entities import User
from core.services import (
    BudgetService,
    CategoryService,
    ExpenseService,
    IncomeService,
    PasswordService,
    TokenService,
    UserService,
)
from core.use_cases.auth import AuthenticationUseCase
from repos import (
    MemoryBudgetService,
    MemoryCategoryService,
    MemoryExpenseService,
    MemoryIncomeService,
    MemoryTokenService,
    MemoryUserService,
)
from services import PasswordBcryptService

header_scheme = APIKeyHeader(name="Authorization", auto_error=False)


def password_service_factory() -> PasswordService:
    return PasswordBcryptService()


def token_service_factory() -> TokenService:
    return MemoryTokenService()


def user_service_factory() -> UserService:
    return MemoryUserService()


def budget_service_factory() -> BudgetService:
    return MemoryBudgetService()


def category_service_factory() -> CategoryService:
    return MemoryCategoryService()


def expense_service_factory() -> ExpenseService:
    return MemoryExpenseService()


def income_service_factory() -> IncomeService:
    return MemoryIncomeService()


async def authentication_user(
    token: Annotated[str | None, Depends(header_scheme)],
    user_service: Annotated[UserService, Depends(user_service_factory)],
    token_service: Annotated[TokenService, Depends(token_service_factory)],
) -> User:
    use_case = AuthenticationUseCase(token_service=token_service, user_service=user_service)
    return await use_case.authenticate(token=token)
