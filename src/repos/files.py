import datetime
import uuid
from pathlib import Path
from typing import Any

from pydantic_core import from_json, to_json

from base import CustomModel
from enums import CategoryType
from repos.abc import (
    BudgetRepo,
    CategoryRepo,
    TokenRepo,
    Total,
    TransactionRepo,
    UserRepo,
)
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.transaction import TransactionSchema
from schemas.user import DetailedUserSchema


def paginate[T](items: list[T], limit: int | None = None, offset: int = 0) -> tuple[Total, list[T]]:
    if limit is None:
        return len(items), items[offset:]
    return len(items), items[offset : offset + limit]


class JsonFileMixin:
    filename: str = "data.json"
    collection: str

    def load(self, model: type[CustomModel] | None = None) -> dict[str, Any]:
        try:
            with Path(self.filename).open() as file:
                all_collections = from_json(file.read())
                collection = all_collections.get(self.collection, {})
        except FileNotFoundError:
            return {}
        return {k: model(**v) for k, v in collection.items()} if model else collection

    def save(self, content: dict[str, Any]) -> None:
        try:
            with Path(self.filename).open() as file:
                all_collections = from_json(file.read())
        except FileNotFoundError:
            all_collections: dict[str, Any] = {}  # type: ignore[no-redef]
        all_collections[self.collection] = content
        with Path(self.filename).open("w") as file:
            file.write(to_json(all_collections, indent=2).decode("utf-8"))


class FileTokenRepo(TokenRepo, JsonFileMixin):
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


class FileUserRepo(UserRepo, JsonFileMixin):
    collection = "users"

    def __init__(self) -> None:
        self._users: dict[str, DetailedUserSchema] = self.load(model=DetailedUserSchema)

    async def add(self, user: DetailedUserSchema) -> DetailedUserSchema:
        self._users[user.id] = user
        self.save(self._users)
        return user

    async def find_by_login(self, login: str) -> DetailedUserSchema | None:
        for user in self._users.values():
            if user.login == login:
                return user
        return None

    async def get(self, user_id: str) -> DetailedUserSchema | None:
        return self._users.get(user_id, None)

    async def update_first_name(self, user_id: str, first_name: str) -> DetailedUserSchema:
        user = self._users[user_id]
        user.first_name = first_name
        self.save(self._users)
        return user

    async def update_last_name(self, user_id: str, last_name: str) -> DetailedUserSchema:
        user = self._users[user_id]
        user.last_name = last_name
        self.save(self._users)
        return user

    async def update_last_login(self, user_id: str, last_login: datetime.datetime) -> DetailedUserSchema:
        user = self._users[user_id]
        user.last_login = last_login
        self.save(self._users)
        return user

    async def change_password_hash(self, user_id: str, password_hash: str) -> DetailedUserSchema:
        user = self._users[user_id]
        user.password_hash = password_hash
        self.save(self._users)
        return user

    async def delete(self, user_id: str) -> None:
        self._users.pop(user_id)
        self.save(self._users)


class FileBudgetRepo(BudgetRepo, JsonFileMixin):
    collection = "budgets"

    def __init__(self) -> None:
        self._budgets: dict[str, BudgetSchema] = self.load(model=BudgetSchema)

    async def add(self, budget: BudgetSchema) -> BudgetSchema:
        self._budgets[budget.id] = budget
        self.save(self._budgets)
        return budget

    async def get(self, budget_id: str) -> BudgetSchema | None:
        return self._budgets.get(budget_id, None)

    async def list_(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[BudgetSchema]]:
        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id]
        if limit is None:
            return len(budgets), budgets[offset:]
        return len(budgets), budgets[offset : offset + limit]

    async def find_by_name(
        self, user_id: str, name: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[BudgetSchema]]:
        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id and budget.name == name]
        return paginate(budgets, limit, offset)

    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[BudgetSchema]]:
        def matches_text(budget: BudgetSchema) -> bool:
            if case_sensitive:
                return text in budget.name or text in budget.description
            return text.lower() in budget.name.lower() or text.lower() in budget.description.lower()

        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id and matches_text(budget)]
        return paginate(budgets, limit, offset)

    async def update(self, budget: BudgetSchema) -> BudgetSchema:
        self._budgets[budget.id] = budget
        self.save(self._budgets)
        return budget

    async def delete(self, budget_id: str) -> BudgetSchema:
        budget = self._budgets.pop(budget_id)
        self.save(self._budgets)
        return budget


class FileCategoryRepo(CategoryRepo, JsonFileMixin):
    collection = "categories"

    def __init__(self) -> None:
        self._categories: dict[str, CategorySchema] = self.load(model=CategorySchema)

    async def add(self, category: CategorySchema) -> CategorySchema:
        self._categories[category.id] = category
        self.save(self._categories)
        return category

    async def get(self, category_id: str) -> CategorySchema | None:
        return self._categories.get(category_id, None)

    async def list_(
        self,
        user_id: str,
        category_type: CategoryType,
        *,
        show_archived: bool = False,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[CategorySchema]]:
        user_categories = [
            category
            for category in self._categories.values()
            if category.user_id == user_id and category.type == category_type
        ]
        if not show_archived:
            user_categories = [category for category in user_categories if not category.is_archived]
        return paginate(user_categories, limit, offset)

    async def find_by_name_and_category(
        self,
        user_id: str,
        name: str,
        category_type: CategoryType | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[CategorySchema]]:
        user_categories = [
            category for category in self._categories.values() if category.user_id == user_id and category.name == name
        ]
        if category_type is not None:
            user_categories = [category for category in user_categories if category.type == category_type]
        return paginate(user_categories, limit, offset)

    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[CategorySchema]]:
        def matches_text(category: CategorySchema) -> bool:
            if case_sensitive:
                return text in category.name or text in category.description
            return text.lower() in category.name.lower() or text.lower() in category.description.lower()

        categories = [
            category for category in self._categories.values() if category.user_id == user_id and matches_text(category)
        ]
        return paginate(categories, limit, offset)

    async def update(self, category: CategorySchema) -> CategorySchema:
        self._categories[category.id] = category
        self.save(self._categories)
        return category

    async def delete(self, category_id: str) -> CategorySchema:
        category = self._categories.pop(category_id)
        self.save(self._categories)
        return category


class FileTransactionRepo(TransactionRepo, JsonFileMixin):
    collection = "incomes"

    def __init__(self) -> None:
        self._transactions: dict[str, TransactionSchema] = self.load(model=TransactionSchema)

    async def add(self, transaction: TransactionSchema) -> TransactionSchema:
        self._transactions[transaction.id] = transaction
        self.save(self._transactions)
        return transaction

    async def get(self, transaction_id: str) -> TransactionSchema | None:
        return self._transactions.get(transaction_id, None)

    async def list_(
        self, user_id: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[TransactionSchema]]:
        incomes = [transaction for transaction in self._transactions.values() if transaction.user_id == user_id]
        return paginate(incomes, limit, offset)

    async def find_by_text(
        self, user_id: str, text: str, *, case_sensitive: bool = False, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[TransactionSchema]]:
        def matches_text(transaction: TransactionSchema) -> bool:
            if case_sensitive:
                return text in transaction.description
            return text.lower() in transaction.description.lower()

        transactions = [
            transaction
            for transaction in self._transactions.values()
            if transaction.user_id == user_id and matches_text(transaction)
        ]
        return paginate(transactions, limit, offset)

    async def update(self, transaction: TransactionSchema) -> TransactionSchema:
        self._transactions[transaction.id] = transaction
        self.save(self._transactions)
        return transaction

    async def delete(self, transaction_id: str) -> TransactionSchema:
        transaction = self._transactions.pop(transaction_id)
        self.save(self._transactions)
        return transaction
