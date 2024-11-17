import datetime
import uuid
from pathlib import Path
from typing import Any

import ujson

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType
from core.services import (
    BudgetService,
    CategoryService,
    ExpenseService,
    IncomeService,
    TokenService,
    Total,
    UserService,
)
from core.utils import UnsetValue, UNSET


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


class FileUserService(UserService, JsonFileMixin):
    collection = "users"

    def __init__(self) -> None:
        self._users: dict[str, User] = self.load()

    async def create(self, first_name: str, last_name: str, login: str, password_hash: str) -> User:
        user = User(first_name=first_name, last_name=last_name, login=login, password_hash=password_hash)
        self._users[user.id] = user
        self.save(self._users)
        return user

    async def find_by_login(self, login: str) -> User | None:
        for user in self._users.values():
            if user.login == login:
                return user
        return None

    async def get(self, user_id: str) -> User | None:
        return self._users.get(user_id, None)

    async def update_first_name(self, user_id: str, first_name: str) -> User:
        user = self._users[user_id]
        user.first_name = first_name
        self.save(self._users)
        return user

    async def update_last_name(self, user_id: str, last_name: str) -> User:
        user = self._users[user_id]
        user.last_name = last_name
        self.save(self._users)
        return user

    async def update_last_login(self, user_id: str, last_login: datetime.datetime) -> User:
        user = self._users[user_id]
        user.last_login = last_login
        self.save(self._users)
        return user

    async def change_password_hash(self, user_id: str, password_hash: str) -> User:
        user = self._users[user_id]
        user.password_hash = password_hash
        self.save(self._users)
        return user

    async def delete(self, user_id: str) -> None:
        self._users.pop(user_id)
        self.save(self._users)


class FileBudgetService(BudgetService, JsonFileMixin):
    collection = "budgets"

    def __init__(self) -> None:
        self._budgets: dict[str, Budget] = self.load()

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        budget = Budget(name=name, description=description, amount=amount, user_id=user_id)
        self._budgets[budget.id] = budget
        self.save(self._budgets)
        return budget

    async def get(self, budget_id: str) -> Budget | None:
        return self._budgets.get(budget_id, None)

    async def find(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[Budget]]:
        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id]
        if limit is None:
            return len(budgets), budgets[offset:]
        return len(budgets), budgets[offset : offset + limit]

    async def find_by_name(
        self, user_id: str, name: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]:
        budgets = [budget for budget in self._budgets.values() if budget.user_id == user_id and budget.name == name]
        return paginate(budgets, limit, offset)

    async def find_by_text(
        self, user_id: str, text: str, limit: int | None = None, offset: int = 0
    ) -> tuple[Total, list[Budget]]:
        budgets = [
            budget
            for budget in self._budgets.values()
            if budget.user_id == user_id and (text in budget.name or text in budget.description)
        ]
        return paginate(budgets, limit, offset)

    async def change_budget(
        self,
        budget_id: str,
        name: str | None = None,
        description: str | None = None,
        amount: float | None = None,
    ) -> Budget:
        budget = self._budgets[budget_id]
        if name is not None:
            budget.name = name
        if description is not None:
            budget.description = description
        if amount is not None:
            budget.amount = amount
        self.save(self._budgets)
        return budget

    async def delete(self, budget_id: str) -> Budget:
        budget = self._budgets.pop(budget_id)
        self.save(self._budgets)
        return budget


class FileCategoryService(CategoryService, JsonFileMixin):
    collection = "categories"

    def __init__(self) -> None:
        self._categories: dict[str, Category] = self.load()

    async def create(
        self, user_id: str, name: str, description: str, category_type: CategoryType, emoji_icon: str | None
    ) -> Category:
        category = Category(
            name=name, description=description, type=category_type, user_id=user_id, emoji_icon=emoji_icon
        )
        self._categories[category.id] = category
        self.save(self._categories)
        return category

    async def get(self, category_id: str) -> Category | None:
        return self._categories.get(category_id, None)

    async def list_(
        self,
        user_id: str,
        category_type: CategoryType,
        *,
        show_archived: bool = False,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]:
        user_categories = [
            category
            for category in self._categories.values()
            if category.user_id == user_id and category.type == category_type
        ]
        if not show_archived:
            user_categories = [category for category in user_categories if not category.is_archived]
        return paginate(user_categories, limit, offset)

    async def find(
        self,
        user_id: str,
        name: str,
        category_type: CategoryType | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> tuple[Total, list[Category]]:
        user_categories = [
            category for category in self._categories.values() if category.user_id == user_id and category.name == name
        ]
        if category_type is not None:
            user_categories = [category for category in user_categories if category.type == category_type]
        return paginate(user_categories, limit, offset)

    async def change_category(
        self,
        category_id: str,
        name: str | UnsetValue = UNSET,
        description: str | UnsetValue = UNSET,
        category_type: CategoryType | UnsetValue = UNSET,
        is_archived: bool | UnsetValue = UNSET,
        emoji_icon: str | None | UnsetValue = UNSET,
    ) -> Category:
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

    async def delete(self, category_id: str) -> None:
        self._categories.pop(category_id)
        self.save(self._categories)


class FileExpenseService(ExpenseService, JsonFileMixin):
    collection = "expenses"

    def __init__(self) -> None:
        self._expenses: dict[str, Expense] = self.load()

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime.datetime
    ) -> Expense:
        expense = Expense(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._expenses[expense.id] = expense
        self.save(self._expenses)
        return expense

    async def get(self, expense_id: str) -> Expense | None:
        return self._expenses[expense_id]

    async def find(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[Expense]]:
        expenses = [expense for expense in self._expenses.values() if expense.user_id == user_id]
        return paginate(expenses, limit, offset)

    async def change_expense(
        self,
        expense_id: str,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Expense:
        expense = self._expenses[expense_id]
        if amount is not None:
            expense.amount = amount
        if category_id is not None:
            expense.category_id = category_id
        if description is not None:
            expense.description = description
        self.save(self._expenses)
        return expense

    async def delete(self, expense_id: str) -> None:
        self._expenses.pop(expense_id)
        self.save(self._expenses)


class FileIncomeService(IncomeService, JsonFileMixin):
    collection = "incomes"

    def __init__(self) -> None:
        self._incomes: dict[str, Income] = self.load()

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime.datetime
    ) -> Income:
        income = Income(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._incomes[income.id] = income
        self.save(self._incomes)
        return income

    async def get(self, income_id: str) -> Income | None:
        return self._incomes[income_id]

    async def find(self, user_id: str, limit: int | None = None, offset: int = 0) -> tuple[Total, list[Income]]:
        incomes = [income for income in self._incomes.values() if income.user_id == user_id]
        return paginate(incomes, limit, offset)

    async def change_income(
        self,
        income_id: str,
        amount: float | None = None,
        category_id: str | None = None,
        description: str | None = None,
    ) -> Income:
        income = self._incomes[income_id]
        if amount is not None:
            income.amount = amount
        if category_id is not None:
            income.category_id = category_id
        if description is not None:
            income.description = description
        self.save(self._incomes)
        return income

    async def delete(self, income_id: str) -> None:
        self._incomes.pop(income_id)
        self.save(self._incomes)
