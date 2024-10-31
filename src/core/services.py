from typing import Protocol

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType


class PasswordService(Protocol):
    @staticmethod
    def hash_password(password: str) -> str: ...


class UserService(Protocol):
    @staticmethod
    async def create(first_name: str, last_name: str, login: str, password_hash: str) -> User: ...

    @staticmethod
    async def find_by_login(login: str) -> User | None: ...

    @staticmethod
    async def get(user_id: str) -> User | None: ...

    @staticmethod
    async def update_first_name(first_name: str) -> User: ...

    @staticmethod
    async def update_last_name(last_name: str) -> User: ...

    @staticmethod
    async def change_password(password: str) -> User: ...

    @staticmethod
    async def delete(user_id: str) -> None: ...


class BudgetService(Protocol):
    @staticmethod
    async def create(name: str, amount: float, user_id: str, description: str | None) -> Budget: ...

    @staticmethod
    async def get(budget_id: str) -> Budget | None: ...

    @staticmethod
    async def find(user_id: str) -> Budget | None: ...

    @staticmethod
    async def change_budget(
        name: str | None = None,
        description: str | None = None,
        amount: float | None = None,
    ) -> Budget: ...

    @staticmethod
    async def delete(budget_id: str) -> None: ...


class CategoryService(Protocol):
    @staticmethod
    async def create(user_id: str, name: str, description: str | None) -> Category: ...

    @staticmethod
    async def get(category_id: str) -> Category | None: ...

    @staticmethod
    async def find(user_id: str, type_: CategoryType | None = None) -> list[Category]: ...

    @staticmethod
    async def change_category(
        name: str | None = None,
        description: str | None = None,
        type_: CategoryType | None = None,
        is_archived: bool | None = None,
    ) -> Category: ...

    @staticmethod
    async def delete(category_id: str) -> None: ...


class ExpenseService(Protocol):
    @staticmethod
    async def create(amount: float, category_id: str, user_id: str, description: str | None = None) -> Expense: ...

    @staticmethod
    async def get(expense_id: str) -> Expense | None: ...

    @staticmethod
    async def find(user_id: str) -> Expense | None: ...

    @staticmethod
    async def change_expense(
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Expense: ...

    @staticmethod
    async def delete(expense_id: str) -> None: ...


class IncomeService(Protocol):
    @staticmethod
    async def create(amount: float, category_id: str, user_id: str, description: str | None = None) -> Income: ...

    @staticmethod
    async def get(income_id: str) -> Income | None: ...

    @staticmethod
    async def find(user_id: str) -> Income | None: ...

    @staticmethod
    async def change_income(
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Income: ...

    @staticmethod
    async def delete(income_id: str) -> None: ...
