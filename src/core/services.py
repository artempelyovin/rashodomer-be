from datetime import datetime
from typing import Protocol

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType


class PasswordService(Protocol):
    @classmethod
    def hash_password(cls, password: str) -> str: ...

    @classmethod
    def check_password(cls, password: str, password_hash: str) -> bool: ...


class UserService(Protocol):
    @classmethod
    async def create(cls, first_name: str, last_name: str, login: str, password_hash: str) -> User: ...

    @classmethod
    async def find_by_login(cls, login: str) -> User | None: ...

    @classmethod
    async def get(cls, user_id: str) -> User | None: ...

    @classmethod
    async def update_first_name(cls, first_name: str) -> User: ...

    @classmethod
    async def update_last_name(cls, last_name: str) -> User: ...

    @classmethod
    async def update_last_login(cls, user_id: str, last_login: datetime) -> User: ...

    @classmethod
    async def change_password(cls, password: str) -> User: ...

    @classmethod
    async def delete(cls, user_id: str) -> None: ...


class BudgetService(Protocol):
    @classmethod
    async def create(cls, name: str, amount: float, user_id: str, description: str | None) -> Budget: ...

    @classmethod
    async def get(cls, budget_id: str) -> Budget | None: ...

    @classmethod
    async def find(cls, user_id: str) -> Budget | None: ...

    @classmethod
    async def change_budget(
        cls,
        name: str | None = None,
        description: str | None = None,
        amount: float | None = None,
    ) -> Budget: ...

    @classmethod
    async def delete(cls, budget_id: str) -> None: ...


class CategoryService(Protocol):
    @classmethod
    async def create(cls, user_id: str, name: str, description: str | None) -> Category: ...

    @classmethod
    async def get(cls, category_id: str) -> Category | None: ...

    @classmethod
    async def find(cls, user_id: str, type_: CategoryType | None = None) -> list[Category]: ...

    @classmethod
    async def change_category(
        cls,
        name: str | None = None,
        description: str | None = None,
        type_: CategoryType | None = None,
        is_archived: bool | None = None,
    ) -> Category: ...

    @classmethod
    async def delete(cls, category_id: str) -> None: ...


class ExpenseService(Protocol):
    @classmethod
    async def create(cls, amount: float, category_id: str, user_id: str, description: str | None = None) -> Expense: ...

    @classmethod
    async def get(cls, expense_id: str) -> Expense | None: ...

    @classmethod
    async def find(cls, user_id: str) -> Expense | None: ...

    @classmethod
    async def change_expense(
        cls,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Expense: ...

    @classmethod
    async def delete(cls, expense_id: str) -> None: ...


class IncomeService(Protocol):
    @classmethod
    async def create(cls, amount: float, category_id: str, user_id: str, description: str | None = None) -> Income: ...

    @classmethod
    async def get(cls, income_id: str) -> Income | None: ...

    @classmethod
    async def find(cls, user_id: str) -> Income | None: ...

    @classmethod
    async def change_income(
        cls,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Income: ...

    @classmethod
    async def delete(cls, income_id: str) -> None: ...
