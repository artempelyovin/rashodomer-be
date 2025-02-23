from abc import ABC, abstractmethod
from datetime import datetime

from enums import CategoryType
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.expense import ExpenseSchema
from schemas.income import IncomeSchema
from schemas.user import DetailedUserSchema
from utils import UNSET, UnsetValue

type Total = int


class TokenRepo(ABC):
    @abstractmethod
    async def create_new_token(self, user_id: str) -> str: ...

    @abstractmethod
    async def get_user_id_by_token(self, token: str) -> str | None: ...


class UserRepo(ABC):
    @abstractmethod
    async def add(self, user: DetailedUserSchema) -> DetailedUserSchema: ...

    @abstractmethod
    async def find_by_login(self, login: str) -> DetailedUserSchema | None: ...

    @abstractmethod
    async def get(self, user_id: str) -> DetailedUserSchema | None: ...

    @abstractmethod
    async def update_first_name(self, user_id: str, first_name: str) -> DetailedUserSchema: ...

    @abstractmethod
    async def update_last_name(self, user_id: str, last_name: str) -> DetailedUserSchema: ...

    @abstractmethod
    async def update_last_login(self, user_id: str, last_login: datetime) -> DetailedUserSchema: ...

    @abstractmethod
    async def change_password_hash(self, user_id: str, password_hash: str) -> DetailedUserSchema: ...

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...


class BudgetRepo(ABC):
    @abstractmethod
    async def add(self, budget: BudgetSchema) -> BudgetSchema: ...

    @abstractmethod
    async def get(self, budget_id: str) -> BudgetSchema | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[BudgetSchema]]: ...

    @abstractmethod
    async def find_by_name(
        self, user_id: str, name: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[BudgetSchema]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[BudgetSchema]]: ...

    @abstractmethod
    async def update_budget(self, budget: BudgetSchema) -> BudgetSchema: ...

    @abstractmethod
    async def delete(self, budget_id: str) -> BudgetSchema: ...


class CategoryRepo(ABC):
    @abstractmethod
    async def add(self, category: CategorySchema) -> CategorySchema: ...

    @abstractmethod
    async def get(self, category_id: str) -> CategorySchema | None: ...

    @abstractmethod
    async def list_(
        self,
        user_id: str,
        category_type: CategoryType,
        *,
        show_archived: bool = False,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[CategorySchema]]: ...

    @abstractmethod
    async def find_by_name_and_category(
        self,
        user_id: str,
        name: str,
        category_type: CategoryType | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[CategorySchema]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[CategorySchema]]: ...

    @abstractmethod
    async def update_category(self, category: CategorySchema) -> CategorySchema: ...

    @abstractmethod
    async def delete(self, category_id: str) -> CategorySchema: ...


class ExpenseRepo(ABC):
    @abstractmethod
    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime
    ) -> ExpenseSchema: ...

    @abstractmethod
    async def get(self, expense_id: str) -> ExpenseSchema | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[ExpenseSchema]]: ...

    @abstractmethod
    async def update_expense(
        self,
        expense_id: str,
        amount: float | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
    ) -> ExpenseSchema: ...

    @abstractmethod
    async def delete(self, expense_id: str) -> None: ...


class IncomeRepo(ABC):
    @abstractmethod
    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime
    ) -> IncomeSchema: ...

    @abstractmethod
    async def get(self, income_id: str) -> IncomeSchema | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[IncomeSchema]]: ...

    @abstractmethod
    async def update_income(
        self,
        income_id: str,
        amount: float | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
    ) -> IncomeSchema:
        pass

    @abstractmethod
    async def delete(self, income_id: str) -> None: ...
