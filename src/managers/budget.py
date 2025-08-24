from datetime import UTC, datetime

from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
)
from models import Budget
from repos.abc import BudgetRepo, Total
from settings import settings


class BudgetManager:
    def __init__(self, budget_repo: BudgetRepo = settings.budget_repo) -> None:
        self.repo = budget_repo

    async def create(
        self, user_id: str, name: str, description: str | None = "", amount: float | None = 0.0
    ) -> Budget:
        if amount < 0:
            raise AmountMustBePositiveError
        _, exist_budgets = await self.repo.find_by_name(user_id=user_id, name=name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        budget = Budget(name=name, description=description, amount=amount, user_id=user_id)
        return await self.repo.add(budget)

    async def get(self, user_id: str, budget_id: str) -> Budget:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return budget

    async def list_(self, user_id: str, limit: int | None, offset: int) -> tuple[Total, list[Budget]]:
        return await self.repo.list_(user_id=user_id, limit=limit, offset=offset)

    async def update(
        self,
        user_id: str,
        budget_id: str,
        *,
        name: str,
        description: str,
        amount: float,
    ) -> Budget:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        if amount < 0:
            raise AmountMustBePositiveError

        budget.name = name
        budget.description = description
        budget.amount = amount
        budget.updated_at = datetime.now(tz=UTC)
        return await self.repo.update(budget)

    async def delete(self, user_id: str, budget_id: str) -> Budget:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return await self.repo.delete(budget_id)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[Budget]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
