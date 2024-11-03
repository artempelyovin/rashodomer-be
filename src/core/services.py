from datetime import datetime
from typing import Protocol

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType


class PasswordService(Protocol):
    def hash_password(self, password: str) -> str: ...

    def check_password(self, password: str, password_hash: str) -> bool: ...


class UserService(Protocol):
    async def create(self, first_name: str, last_name: str, login: str, password_hash: str) -> User: ...

    async def find_by_login(self, login: str) -> User | None: ...

    async def get(self, user_id: str) -> User | None: ...

    async def update_first_name(self, user_id: str, first_name: str) -> User: ...

    async def update_last_name(self, user_id: str, last_name: str) -> User: ...

    async def update_last_login(self, user_id: str, last_login: datetime) -> User: ...

    async def change_password(self, password: str) -> User: ...

    async def delete(self, user_id: str) -> None: ...


class BudgetService(Protocol):
    async def create(self, name: str, amount: float, user_id: str, description: str | None) -> Budget: ...

    async def get(self, budget_id: str) -> Budget | None: ...

    async def find(self, user_id: str) -> Budget | None: ...

    async def change_budget(
        self,
        name: str | None = None,
        description: str | None = None,
        amount: float | None = None,
    ) -> Budget: ...

    async def delete(self, budget_id: str) -> None: ...


class CategoryService(Protocol):
    async def create(self, user_id: str, name: str, description: str | None) -> Category: ...

    async def get(self, category_id: str) -> Category | None: ...

    async def find(self, user_id: str, type_: CategoryType | None = None) -> list[Category]: ...

    async def change_category(
        self,
        name: str | None = None,
        description: str | None = None,
        type_: CategoryType | None = None,
        is_archived: bool | None = None,
    ) -> Category: ...

    async def delete(self, category_id: str) -> None: ...


class ExpenseService(Protocol):
    async def create(
        self, amount: float, category_id: str, user_id: str, description: str | None = None
    ) -> Expense: ...

    async def get(self, expense_id: str) -> Expense | None: ...

    async def find(self, user_id: str) -> Expense | None: ...

    async def change_expense(
        self,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Expense: ...

    async def delete(self, expense_id: str) -> None: ...


class IncomeService(Protocol):
    async def create(self, amount: float, category_id: str, user_id: str, description: str | None = None) -> Income: ...

    async def get(self, income_id: str) -> Income | None: ...

    async def find(self, user_id: str) -> Income | None: ...

    async def change_income(
        self,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Income: ...

    async def delete(self, income_id: str) -> None: ...
