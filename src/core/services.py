from abc import ABC, abstractmethod
from datetime import datetime

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType


class PasswordService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def check_password(self, password: str, password_hash: str) -> bool: ...


class UserService(ABC):
    @abstractmethod
    async def create(self, first_name: str, last_name: str, login: str, password_hash: str) -> User: ...

    @abstractmethod
    async def find_by_login(self, login: str) -> User | None: ...

    @abstractmethod
    async def get(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def update_first_name(self, user_id: str, first_name: str) -> User: ...

    @abstractmethod
    async def update_last_name(self, user_id: str, last_name: str) -> User: ...

    @abstractmethod
    async def update_last_login(self, user_id: str, last_login: datetime) -> User: ...

    @abstractmethod
    async def change_password(self, password: str) -> User: ...

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...


class BudgetService(ABC):
    @abstractmethod
    async def create(self, name: str, amount: float, user_id: str, description: str | None) -> Budget: ...

    @abstractmethod
    async def get(self, budget_id: str) -> Budget | None: ...

    @abstractmethod
    async def find(self, user_id: str) -> Budget | None: ...

    @abstractmethod
    async def change_budget(
        self,
        name: str | None = None,
        description: str | None = None,
        amount: float | None = None,
    ) -> Budget: ...

    @abstractmethod
    async def delete(self, budget_id: str) -> None: ...


class CategoryService(ABC):
    @abstractmethod
    async def create(self, user_id: str, name: str, description: str | None) -> Category: ...

    @abstractmethod
    async def get(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def find(self, user_id: str, type_: CategoryType | None = None) -> list[Category]: ...

    @abstractmethod
    async def change_category(
        self,
        name: str | None = None,
        description: str | None = None,
        type_: CategoryType | None = None,
        is_archived: bool | None = None,
    ) -> Category: ...

    @abstractmethod
    async def delete(self, category_id: str) -> None: ...


class ExpenseService(ABC):
    @abstractmethod
    async def create(
        self, amount: float, category_id: str, user_id: str, description: str | None = None
    ) -> Expense: ...

    @abstractmethod
    async def get(self, expense_id: str) -> Expense | None: ...

    @abstractmethod
    async def find(self, user_id: str) -> Expense | None: ...

    @abstractmethod
    async def change_expense(
        self,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Expense: ...

    @abstractmethod
    async def delete(self, expense_id: str) -> None: ...


class IncomeService(ABC):
    @abstractmethod
    async def create(self, amount: float, category_id: str, user_id: str, description: str | None = None) -> Income: ...

    @abstractmethod
    async def get(self, income_id: str) -> Income | None: ...

    @abstractmethod
    async def find(self, user_id: str) -> Income | None: ...

    @abstractmethod
    async def change_income(
        self,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Income: ...

    @abstractmethod
    async def delete(self, income_id: str) -> None: ...
