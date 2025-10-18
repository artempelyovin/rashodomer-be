from datetime import UTC, datetime

from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
)
from models import BudgetSchema
from repos.abc import BudgetRepo, Total
from settings import settings
from utils import UnsetValue


class BudgetManager:
    def __init__(self, budget_repo: BudgetRepo = settings.budget_repo) -> None:
        self.repo = budget_repo

    async def create(
        self, user_id: str, name: str, description: str | None = "", amount: float | None = 0.0
    ) -> BudgetSchema:
        if amount < 0:
            raise AmountMustBePositiveError
        _, exist_budgets = await self.repo.find_by_name(user_id=user_id, name=name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        budget = BudgetSchema(name=name, description=description, amount=amount, user_id=user_id)
        return await self.repo.add(budget)

    async def get(self, user_id: str, budget_id: str) -> BudgetSchema:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return budget

    async def list_(self, user_id: str, limit: int | None, offset: int) -> tuple[Total, list[BudgetSchema]]:
        return await self.repo.list_(user_id=user_id, limit=limit, offset=offset)

    async def update(
        self,
        user_id: str,
        budget_id: str,
        *,
        name: str | UnsetValue,
        description: str | UnsetValue,
        amount: float | UnsetValue,
    ) -> BudgetSchema:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        if not isinstance(amount, UnsetValue) and amount < 0:
            raise AmountMustBePositiveError

        if not isinstance(name, UnsetValue):
            budget.name = name
        if not isinstance(description, UnsetValue):
            budget.description = description
        if not isinstance(amount, UnsetValue):
            budget.amount = amount
        budget.updated_at = datetime.now(tz=UTC)
        return await self.repo.update(budget)

    async def delete(self, user_id: str, budget_id: str) -> BudgetSchema:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return await self.repo.delete(budget_id)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[BudgetSchema]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
