from abc import ABC, abstractmethod
from datetime import datetime

from enums import CategoryType
from models import Budget, Category, DetailedUser, Transaction

type Total = int


class TokenRepo(ABC):
    @abstractmethod
    async def create_new_token(self, user_id: str) -> str: ...

    @abstractmethod
    async def get_user_id_by_token(self, token: str) -> str | None: ...


class UserRepo(ABC):
    @abstractmethod
    async def add(self, user: DetailedUser) -> DetailedUser: ...

    @abstractmethod
    async def find_by_login(self, login: str) -> DetailedUser | None: ...

    @abstractmethod
    async def get(self, user_id: str) -> DetailedUser | None: ...

    @abstractmethod
    async def update_first_name(self, user_id: str, first_name: str) -> DetailedUser: ...

    @abstractmethod
    async def update_last_name(self, user_id: str, last_name: str) -> DetailedUser: ...

    @abstractmethod
    async def update_last_login(self, user_id: str, last_login: datetime) -> DetailedUser: ...

    @abstractmethod
    async def change_password_hash(self, user_id: str, password_hash: str) -> DetailedUser: ...

    @abstractmethod
    async def delete(self, user_id: str) -> None: ...


class BudgetRepo(ABC):
    @abstractmethod
    async def add(self, budget: Budget) -> Budget: ...

    @abstractmethod
    async def get(self, budget_id: str) -> Budget | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def find_by_name(
        self, user_id: str, name: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]: ...

    @abstractmethod
    async def update(self, budget: Budget) -> Budget: ...

    @abstractmethod
    async def delete(self, budget_id: str) -> Budget: ...


class CategoryRepo(ABC):
    @abstractmethod
    async def add(self, category: Category) -> Category: ...

    @abstractmethod
    async def get(self, category_id: str) -> Category | None: ...

    @abstractmethod
    async def list_(
        self,
        user_id: str,
        *,
        category_type: CategoryType | None = None,
        show_archived: bool = False,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def find_by_name_and_category(
        self,
        user_id: str,
        name: str,
        category_type: CategoryType | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Category]]: ...

    @abstractmethod
    async def update(self, category: Category) -> Category: ...

    @abstractmethod
    async def delete(self, category_id: str) -> Category: ...


class TransactionRepo(ABC):
    @abstractmethod
    async def add(self, transaction: Transaction) -> Transaction: ...

    @abstractmethod
    async def get(self, transaction_id: str) -> Transaction | None: ...

    @abstractmethod
    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Transaction]]: ...

    @abstractmethod
    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Transaction]]: ...

    @abstractmethod
    async def update(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    async def delete(self, income_id: str) -> Transaction: ...
