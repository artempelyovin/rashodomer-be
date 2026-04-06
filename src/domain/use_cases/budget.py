import logging
from decimal import Decimal

from domain.errors import BudgetNotFoundError, EmptyNameError, NegativeBalanceError
from domain.models.budget import Budget
from domain.repos.budget import BudgetRepo
from domain.utils import UNSET, Unset, uuid4_str

logger = logging.getLogger(__name__)


class CreateBudget:
    def __init__(self, repo: BudgetRepo) -> None:
        self._repo = repo

    async def execute(self, name: str, balance: Decimal, user_id: str, description: str | None = None) -> Budget:
        if not name or not name.strip():
            raise EmptyNameError(field="name")
        if balance < 0:
            raise NegativeBalanceError(balance)
        budget_id = uuid4_str()
        budget = Budget(
            id=budget_id,
            name=name,
            balance=balance,
            user_id=user_id,
            description=description,
        )
        await self._repo.create(budget)
        logger.info("Created budget %s for user %s", budget_id, user_id)
        return budget


class GetBudget:
    def __init__(self, repo: BudgetRepo) -> None:
        self._repo = repo

    async def execute(self, budget_id: str) -> Budget:
        budget = await self._repo.get_by_id(budget_id)
        if budget is None:
            raise BudgetNotFoundError(budget_id)
        logger.info("Retrieved budget %s", budget_id)
        return budget


class ListBudgets:
    def __init__(self, repo: BudgetRepo) -> None:
        self._repo = repo

    async def execute(self, user_id: str) -> list[Budget]:
        budgets = await self._repo.get_by_user_id(user_id)
        logger.info("Listed %d budgets for user %s", len(budgets), user_id)
        return budgets


class UpdateBudget:
    def __init__(self, repo: BudgetRepo) -> None:
        self._repo = repo

    async def execute(
        self,
        budget_id: str,
        name: str | Unset = UNSET,
        balance: Decimal | Unset = UNSET,
        description: str | None | Unset = UNSET,
    ) -> Budget:
        budget = await self._repo.get_by_id(budget_id)
        if budget is None:
            raise BudgetNotFoundError(budget_id)

        if not isinstance(name, Unset):
            if not name.strip():
                raise EmptyNameError(field="name")
            budget.name = name
        if not isinstance(balance, Unset):
            if balance < 0:
                raise NegativeBalanceError(balance)
            budget.balance = balance
        if not isinstance(description, Unset):
            budget.description = description

        await self._repo.update(budget)
        logger.info("Updated budget %s", budget_id)
        return budget


class DeleteBudget:
    def __init__(self, repo: BudgetRepo) -> None:
        self._repo = repo

    async def execute(self, budget_id: str) -> None:
        existing = await self._repo.get_by_id(budget_id)
        if existing is None:
            raise BudgetNotFoundError(budget_id)
        await self._repo.delete(budget_id)
        logger.info("Deleted budget %s", budget_id)
