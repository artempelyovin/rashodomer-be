import uuid
from pathlib import Path
from typing import Any

import ujson

from core.entities import Budget, Category, Transaction, User
from core.enums import TransactionType
from core.repos import BudgetRepository, CategoryRepository, TransactionRepository, UserRepository
from core.services import (
    TokenService,
    Total,
)
from core.utils import UNSET, UnsetValue


def paginate[T](items: list[T], limit: int | None = None, offset: int = 0) -> tuple[Total, list[T]]:
    if limit is None:
        return len(items), items[offset:]
    return len(items), items[offset : offset + limit]


class JsonFileMixin:
    filename: str = "data.json"
    collection: str

    @staticmethod
    def to_dict(content: dict[str, User]) -> dict[str, Any]:
        return {k: repr(v) for k, v in content.items()}

    @staticmethod
    def from_dict(content: dict[str, Any]) -> dict[str, User]:
        return {k: eval(v) for k, v in content.items()}  # noqa: S307

    def load(self) -> dict[str, Any]:
        all_collections: dict[str, Any] = {}
        try:
            with Path(self.filename).open() as file:
                all_collections = ujson.load(file)
        except FileNotFoundError:
            pass
        return self.from_dict(all_collections.get(self.collection, {}))

    def save(self, content: dict[str, Any]) -> None:
        all_collections: dict[str, Any] = {}
        try:
            with Path(self.filename).open() as file:
                all_collections = ujson.load(file)
        except FileNotFoundError:
            pass
        all_collections[self.collection] = self.to_dict(content)
        with Path(self.filename).open("w") as file:
            ujson.dump(all_collections, file, indent=4, ensure_ascii=False)


class FileTokenService(TokenService, JsonFileMixin):
    collection = "tokens"

    def __init__(self) -> None:
        self._tokens: dict[str, str] = self.load()  # format: user_id: token

    async def create_new_token(self, user_id: str) -> str:
        self._tokens[user_id] = str(uuid.uuid4())
        self.save(self._tokens)
        return self._tokens[user_id]

    async def get_user_id_by_token(self, token: str) -> str | None:
        for user_id, exist_token in self._tokens.items():
            if exist_token == token:
                return user_id
        return None


class FileUserRepository(UserRepository, JsonFileMixin):
    collection = "users"

    def __init__(self) -> None:
        self._users: dict[str, User] = self.load()

    async def create(self, entity: User) -> User:
        self._users[entity.id] = entity
        self.save(self._users)
        return entity

    async def update(self, updated_entity: User) -> User:
        self._users[updated_entity.id] = updated_entity
        self.save(self._users)
        return updated_entity

    async def get(self, entity_id: str) -> User | None:
        return self._users.get(entity_id, None)

    async def delete(self, entity_id: str) -> User:
        user = self._users.pop(entity_id)
        self.save(self._users)
        return user

    async def find_by_login(self, login: str) -> User | None:
        for user in self._users.values():
            if user.login == login:
                return user
        return None


class FileBudgetRepository(BudgetRepository, JsonFileMixin):
    collection = "budgets"

    def __init__(self) -> None:
        self._budgets: dict[str, Budget] = self.load()

    async def create(self, entity: Budget) -> Budget:
        self._budgets[entity.id] = entity
        self.save(self._budgets)
        return entity

    async def update(self, updated_entity: Budget) -> Budget:
        self._budgets[updated_entity.id] = updated_entity
        self.save(self._budgets)
        return updated_entity

    async def get(self, entity_id: str) -> Budget | None:
        return self._budgets.get(entity_id, None)

    async def delete(self, entity_id: str) -> Budget:
        budget = self._budgets.pop(entity_id)
        self.save(self._budgets)
        return budget

    async def list_(
        self, user_id: str, *, name: str | UnsetValue = UNSET, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]:
        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id]
        if not isinstance(name, UnsetValue):
            budgets = [budget for budget in budgets if budget.name == name]
        if limit is None:
            return len(budgets), budgets[offset:]
        return len(budgets), budgets[offset : offset + limit]

    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]:
        def matches_text(budget: Budget) -> bool:
            if case_sensitive:
                return text in budget.name or text in budget.description
            return text.lower() in budget.name.lower() or text.lower() in budget.description.lower()

        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id and matches_text(budget)]
        return paginate(budgets, limit, offset)


class FileCategoryRepository(CategoryRepository, JsonFileMixin):
    collection = "categories"

    def __init__(self) -> None:
        self._categories: dict[str, Category] = self.load()

    async def create(self, entity: Category) -> Category:
        self._categories[entity.id] = entity
        self.save(self._categories)
        return entity

    async def update(self, updated_entity: Category) -> Category:
        self._categories[updated_entity.id] = updated_entity
        self.save(self._categories)
        return updated_entity

    async def get(self, entity_id: str) -> Category | None:
        return self._categories.get(entity_id, None)

    async def delete(self, entity_id: str) -> Category:
        category = self._categories.pop(entity_id)
        self.save(self._categories)
        return category

    async def list_(
        self,
        user_id: str,
        transaction_type: TransactionType,
        *,
        show_archived: bool = False,
        name: str | UnsetValue = UNSET,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]:
        user_categories = [
            category
            for category in self._categories.values()
            if category.user_id == user_id and category.type == transaction_type
        ]
        if not show_archived:
            user_categories = [category for category in user_categories if not category.is_archived]
        if not isinstance(name, UnsetValue):
            user_categories = [category for category in user_categories if category.name == name]
        return paginate(user_categories, limit, offset)

    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Category]]:
        def matches_text(category: Category) -> bool:
            if case_sensitive:
                return text in category.name or text in category.description
            return text.lower() in category.name.lower() or text.lower() in category.description.lower()

        categories = [
            category for category in self._categories.values() if category.user_id == user_id and matches_text(category)
        ]
        return paginate(categories, limit, offset)


class FileTransactionRepository(TransactionRepository, JsonFileMixin):
    collection = "transactions"

    def __init__(self) -> None:
        self._transactions: dict[str, Transaction] = self.load()

    async def create(self, entity: Transaction) -> Transaction:
        self._transactions[entity.id] = entity
        self.save(self._transactions)
        return entity

    async def update(self, updated_entity: Transaction) -> Transaction:
        self._transactions[updated_entity.id] = updated_entity
        self.save(self._transactions)
        return updated_entity

    async def get(self, entity_id: str) -> Transaction | None:
        return self._transactions.get(entity_id, None)

    async def delete(self, entity_id: str) -> Transaction:
        transaction = self._transactions.pop(entity_id)
        self.save(self._transactions)
        return transaction

    async def list_(
        self,
        user_id: str,
        *,
        type_: TransactionType | UnsetValue = UNSET,
        budget_id: str | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Transaction]]:
        expenses = [expense for expense in self._transactions.values() if expense.user_id == user_id]
        if not isinstance(type_, UnsetValue):
            expenses = [e for e in expenses if e.type == type_]
        if not isinstance(budget_id, UnsetValue):
            expenses = [e for e in expenses if e.budget_id == budget_id]
        if not isinstance(category_id, UnsetValue):
            expenses = [e for e in expenses if e.category_id == category_id]
        return paginate(expenses, limit, offset)
