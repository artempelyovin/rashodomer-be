from abc import ABC, abstractmethod
from datetime import datetime

from enums import CategoryType
from models import BudgetSchema, CategorySchema, DetailedUserSchema, TransactionSchema

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
    async def update(self, budget: BudgetSchema) -> BudgetSchema: ...

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
        *,
        category_type: CategoryType | None = None,
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
    async def update(self, category: CategorySchema) -> CategorySchema: ...

    @abstractmethod
    async def delete(self, category_id: str) -> CategorySchema: ...


class TransactionRepo(ABC):
    @abstractmethod
    async def add(self, transaction: TransactionSchema) -> TransactionSchema: ...

    @abstractmethod
    async def get(self, transaction_id: str) -> TransactionSchema | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[TransactionSchema]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[TransactionSchema]]: ...

    @abstractmethod
    async def update(self, transaction: TransactionSchema) -> TransactionSchema:
        pass

    @abstractmethod
    async def delete(self, income_id: str) -> TransactionSchema: ...
