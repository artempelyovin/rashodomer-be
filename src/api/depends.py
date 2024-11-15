from core.services import (
    BudgetService,
    CategoryService,
    ExpenseService,
    IncomeService,
    PasswordService,
    TokenService,
    UserService,
)
from repos import (
    MemoryBudgetService,
    MemoryCategoryService,
    MemoryExpenseService,
    MemoryIncomeService,
    MemoryTokenService,
    MemoryUserService,
)
from services import PasswordBcryptService


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
