from abc import ABC, abstractmethod

from domain.models.category import Category
from domain.models.transaction import TransactionType


class CategoryRepo(ABC):
    @abstractmethod
    async def create(self, category: Category) -> None: ...

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: str, transaction_type: TransactionType | None = None) -> list[Category]: ...

    @abstractmethod
    async def update(self, category: Category) -> None: ...

    @abstractmethod
    async def delete(self, category_id: str) -> None: ...
