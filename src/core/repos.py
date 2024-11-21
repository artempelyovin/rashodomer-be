from abc import ABC, abstractmethod

from core.entities import Budget, Category, Transaction, User
from core.enums import TransactionType
from core.services import Total
from core.utils import UNSET, UnsetValue


class BaseRepository[T](ABC):
    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def update(self, updated_entity: T) -> T: ...

    @abstractmethod
    async def get(self, entity_id: str) -> T | None: ...

    @abstractmethod
    async def delete(self, entity_id: str) -> T: ...


class UserRepository(BaseRepository[User]):
    @abstractmethod
    async def find_by_login(self, login: str) -> User | None: ...


class BudgetRepository(BaseRepository[Budget]):
    @abstractmethod
    async def list_(
        self, user_id: str, *, name: str | UnsetValue = UNSET, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...


class CategoryRepository(BaseRepository[Category]):
    @abstractmethod
    async def list_(
        self,
        user_id: str,
        transaction_type: TransactionType,
        *,
        show_archived: bool = False,
        name: str | UnsetValue = UNSET,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Category]]: ...


class TransactionRepository(BaseRepository[Transaction]):
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
