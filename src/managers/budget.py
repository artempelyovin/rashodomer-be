from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
)
from repos.abc import BudgetRepo, Total
from schemas.budget import BudgetSchema, CreateBudgetSchema
from utils import UnsetValue


class BudgetManager:
    def __init__(self, budget_repo: BudgetRepo) -> None:
        self.repo = budget_repo

    async def create(self, user_id: str, data: CreateBudgetSchema) -> BudgetSchema:
        if data.amount < 0:
            raise AmountMustBePositiveError
        _, exist_budgets = await self.repo.find_by_name(user_id=user_id, name=data.name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=data.name)
        budget = BudgetSchema(name=data.name, description=data.description, amount=data.amount, user_id=user_id)
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
        return await self.repo.update_budget(budget_id=budget_id, name=name, description=description, amount=amount)

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
