from datetime import datetime

from core.entities import Budget, Category, Expense, Income, User
from core.enums import CategoryType
from core.services import BudgetService, CategoryService, ExpenseService, IncomeService, UserService


class MemoryUserService(UserService):
    _users: dict[str, User] = {}  # noqa: RUF012

    async def create(self, first_name: str, last_name: str, login: str, password_hash: str) -> User:
        user = User(first_name=first_name, last_name=last_name, login=login, password_hash=password_hash)
        self._users[user.id] = user
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
        return user

    async def update_last_name(self, user_id: str, last_name: str) -> User:
        user = self._users[user_id]
        user.last_name = last_name
        return user

    async def update_last_login(self, user_id: str, last_login: datetime) -> User:
        user = self._users[user_id]
        user.last_login = last_login
        return user

    async def change_password_hash(self, user_id: str, password_hash: str) -> User:
        user = self._users[user_id]
        user.password_hash = password_hash
        return user

    async def delete(self, user_id: str) -> None:
        self._users.pop(user_id)


class MemoryBudgetService(BudgetService):
    _budgets: dict[str, Budget] = {}  # noqa: RUF012

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        budget = Budget(name=name, description=description, amount=amount, user_id=user_id)
        self._budgets[budget.id] = budget
        return budget

    async def get(self, budget_id: str) -> Budget | None:
        return self._budgets[budget_id]

    async def find(self, user_id: str) -> list[Budget]:
        return [budget for budget in self._budgets.values() if budget.user_id == user_id]

    async def find_by_name(self, user_id: str, name: str) -> list[Budget]:
        return [budget for budget in self._budgets.values() if budget.user_id == user_id and budget.name == name]

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
        return budget

    async def delete(self, budget_id: str) -> None:
        self._budgets.pop(budget_id)


class MemoryCategoryService(CategoryService):
    _categories: dict[str, Category] = {}  # noqa: RUF012

    async def create(self, user_id: str, name: str, description: str, category_type: CategoryType) -> Category:
        category = Category(name=name, description=description, type=category_type, user_id=user_id)
        self._categories[category.id] = category
        return category

    async def get(self, category_id: str) -> Category | None:
        return self._categories[category_id]

    async def find(self, user_id: str, category_type: CategoryType | None = None) -> list[Category]:
        user_categories = [
            category
            for category in self._categories.values()
            if category.user_id == user_id and category.type == category_type
        ]
        if category_type is None:
            return user_categories
        return [category for category in user_categories if category.type == category_type]

    async def change_category(
        self,
        category_id: str,
        name: str | None = None,
        description: str | None = None,
        category_type: CategoryType | None = None,
        is_archived: bool | None = None,
    ) -> Category:
        category = self._categories[category_id]
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        if category_type is not None:
            category.type = category_type
        if is_archived is not None:
            category.is_archived = is_archived
        return category

    async def delete(self, category_id: str) -> None:
        self._categories.pop(category_id)


class MemoryExpenseService(ExpenseService):
    _expenses: dict[str, Expense] = {}  # noqa: RUF012

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime
    ) -> Expense:
        expense = Expense(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._expenses[expense.id] = expense
        return expense

    async def get(self, expense_id: str) -> Expense | None:
        return self._expenses[expense_id]

    async def find(self, user_id: str) -> list[Expense]:
        return [expense for expense in self._expenses.values() if expense.user_id == user_id]

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
        return expense

    async def delete(self, expense_id: str) -> None:
        self._expenses.pop(expense_id)


class MemoryIncomeService(IncomeService):
    _incomes: dict[str, Income] = {}  # noqa: RUF012

    async def create(
        self, amount: float, description: str, category_id: str, user_id: str, timestamp: datetime
    ) -> Income:
        income = Income(
            amount=amount, description=description, category_id=category_id, user_id=user_id, timestamp=timestamp
        )
        self._incomes[income.id] = income
        return income

    async def get(self, income_id: str) -> Income | None:
        return self._incomes[income_id]

    async def find(self, user_id: str) -> list[Income]:
        return [income for income in self._incomes.values() if income.user_id == user_id]

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
        return income

    async def delete(self, income_id: str) -> None:
        self._incomes.pop(income_id)
