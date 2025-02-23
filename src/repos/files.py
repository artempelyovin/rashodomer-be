import datetime
import uuid
from pathlib import Path
from typing import Any

import ujson

from enums import CategoryType
from repos.abc import (
    BudgetRepo,
    CategoryRepo,
    ExpenseRepo,
    IncomeRepo,
    TokenRepo,
    Total,
    UserRepo,
)
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.expense import ExpenseSchema
from schemas.income import IncomeSchema
from schemas.user import UserSchema
from utils import UNSET, UnsetValue


def paginate[T](items: list[T], limit: int | None = None, offset: int = 0) -> tuple[Total, list[T]]:
    if limit is None:
        return len(items), items[offset:]
    return len(items), items[offset : offset + limit]


class JsonFileMixin:
    filename: str = "data.json"
    collection: str

    @staticmethod
    def to_dict(content: dict[str, UserSchema]) -> dict[str, Any]:
        return {k: repr(v) for k, v in content.items()}

    @staticmethod
    def from_dict(content: dict[str, Any]) -> dict[str, UserSchema]:
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
        self._users: dict[str, UserSchema] = self.load()

    async def add(self, user: UserSchema) -> UserSchema:
        self._users[user.id] = user
        self.save(self._users)
        return user

    async def find_by_login(self, login: str) -> UserSchema | None:
        for user in self._users.values():
            if user.login == login:
                return user
        return None

    async def get(self, user_id: str) -> UserSchema | None:
        return self._users.get(user_id, None)

    async def update_first_name(self, user_id: str, first_name: str) -> UserSchema:
        user = self._users[user_id]
        user.first_name = first_name
        self.save(self._users)
        return user

    async def update_last_name(self, user_id: str, last_name: str) -> UserSchema:
        user = self._users[user_id]
        user.last_name = last_name
        self.save(self._users)
        return user

    async def update_last_login(self, user_id: str, last_login: datetime.datetime) -> UserSchema:
        user = self._users[user_id]
        user.last_login = last_login
        self.save(self._users)
        return user

    async def change_password_hash(self, user_id: str, password_hash: str) -> UserSchema:
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
        self._budgets: dict[str, BudgetSchema] = self.load()

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

    async def update_budget(
        self,
        budget_id: str,
        name: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
        amount: float | UnsetValue = UNSET,
    ) -> BudgetSchema:
        budget = self._budgets[budget_id]
        if not isinstance(name, UnsetValue):
            budget.name = name
        if not isinstance(description, UnsetValue):
            budget.description = description
        if not isinstance(amount, UnsetValue):
            budget.amount = amount
        self.save(self._budgets)
        return budget

    async def delete(self, budget_id: str) -> BudgetSchema:
        budget = self._budgets.pop(budget_id)
        self.save(self._budgets)
        return budget


class FileCategoryRepo(CategoryRepo, JsonFileMixin):
    collection = "categories"

    def __init__(self) -> None:
        self._categories: dict[str, CategorySchema] = self.load()

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

    async def update_category(
        self,
        category_id: str,
        name: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
        category_type: CategoryType | UnsetValue = UNSET,
        is_archived: bool | UnsetValue = UNSET,
        emoji_icon: str | None | UnsetValue = UNSET,
    ) -> CategorySchema:
        category = self._categories[category_id]
        if not isinstance(name, UnsetValue):
            category.name = name
        if not isinstance(description, UnsetValue):
            category.description = description
        if not isinstance(category_type, UnsetValue):
            category.type = category_type
        if not isinstance(is_archived, UnsetValue):
            category.is_archived = is_archived
        if not isinstance(emoji_icon, UnsetValue):
            category.emoji_icon = emoji_icon
        self.save(self._categories)
        return category

    async def delete(self, category_id: str) -> CategorySchema:
        category = self._categories.pop(category_id)
        self.save(self._categories)
        return category


class FileExpenseRepo(ExpenseRepo, JsonFileMixin):
    collection = "expenses"

    def __init__(self) -> None:
        self._expenses: dict[str, ExpenseSchema] = self.load()

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime.datetime
    ) -> ExpenseSchema:
        expense = ExpenseSchema(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._expenses[expense.id] = expense
        self.save(self._expenses)
        return expense

    async def get(self, expense_id: str) -> ExpenseSchema | None:
        return self._expenses[expense_id]

    async def list_(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[ExpenseSchema]]:
        expenses = [expense for expense in self._expenses.values() if expense.user_id == user_id]
        return paginate(expenses, limit, offset)

    async def update_expense(
        self,
        expense_id: str,
        amount: float | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
    ) -> ExpenseSchema:
        expense = self._expenses[expense_id]
        if not isinstance(amount, UnsetValue):
            expense.amount = amount
        if not isinstance(category_id, UnsetValue):
            expense.category_id = category_id
        if not isinstance(description, UnsetValue):
            expense.description = description
        self.save(self._expenses)
        return expense

    async def delete(self, expense_id: str) -> None:
        self._expenses.pop(expense_id)
        self.save(self._expenses)


class FileIncomeRepo(IncomeRepo, JsonFileMixin):
    collection = "incomes"

    def __init__(self) -> None:
        self._incomes: dict[str, IncomeSchema] = self.load()

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime.datetime
    ) -> IncomeSchema:
        income = IncomeSchema(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._incomes[income.id] = income
        self.save(self._incomes)
        return income

    async def get(self, income_id: str) -> IncomeSchema | None:
        return self._incomes[income_id]

    async def list_(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[IncomeSchema]]:
        incomes = [income for income in self._incomes.values() if income.user_id == user_id]
        return paginate(incomes, limit, offset)

    async def update_income(
        self,
        income_id: str,
        amount: float | UnsetValue = UNSET,
        category_id: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
    ) -> IncomeSchema:
        income = self._incomes[income_id]
        if not isinstance(amount, UnsetValue):
            income.amount = amount
        if not isinstance(category_id, UnsetValue):
            income.category_id = category_id
        if not isinstance(description, UnsetValue):
            income.description = description
        self.save(self._incomes)
        return income

    async def delete(self, income_id: str) -> None:
        self._incomes.pop(income_id)
        self.save(self._incomes)
