from abc import ABC, abstractmethod
from datetime import datetime

from core.entities import User, Budget, Category, Transaction
from core.enums import TransactionType
from core.services import Total
from core.utils import UnsetValue, UNSET


class UserRepository(ABC):
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
    async def change_password_hash(self, user_id: str, password_hash: str) -> User: ...

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...


class BudgetRepository(ABC):
    @abstractmethod
    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget: ...

    @abstractmethod
    async def get(self, budget_id: str) -> Budget | None: ...

    @abstractmethod
    async def list_(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def find_by_name(
        self, user_id: str, name: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def update_budget(
        self,
        budget_id: str,
        name: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
        amount: float | UnsetValue = UNSET,
    ) -> Budget: ...

    @abstractmethod
    async def delete(self, budget_id: str) -> Budget: ...


class CategoryRepository(ABC):
    @abstractmethod
    async def create(
        self, user_id: str, name: str, description: str, transaction_type: TransactionType, emoji_icon: str | None
    ) -> Category: ...

    @abstractmethod
    async def get(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def list_(
        self,
        user_id: str,
        transaction_type: TransactionType,
        *,
        show_archived: bool = False,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def find_by_name_and_category(
        self,
        user_id: str,
        name: str,
        transaction_type: TransactionType | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def update_category(
        self,
        category_id: str,
        name: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
        transaction_type: TransactionType | UnsetValue = UNSET,
        is_archived: bool | UnsetValue = UNSET,
        emoji_icon: str | None | UnsetValue = UNSET,
    ) -> Category: ...

    @abstractmethod
    async def delete(self, category_id: str) -> Category: ...


class TransactionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        amount: float,
        description: str,
        transaction_type: TransactionType,
        budget_id: str,
        category_id: str,
        user_id: str,
        timestamp: datetime,
    ) -> Transaction: ...

    @abstractmethod
    async def get(self, transaction_id: str) -> Transaction | None: ...

    @abstractmethod
    async def list_(
        self,
        user_id: str,
        *,
        type_: TransactionType | UnsetValue = UNSET,
        budget_id: str | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Transaction]]: ...

    @abstractmethod
    async def update(
        self,
        expense_id: str,
        amount: float | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
    ) -> Transaction: ...

    @abstractmethod
    async def delete(self, transaction_id: str) -> Transaction: ...
