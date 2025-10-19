from datetime import UTC, datetime

from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
)
from repos.abc import BudgetRepo, Total
from schemas.budget import BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema


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

    async def update(self, user_id: str, budget_id: str, params: UpdateBudgetSchema) -> BudgetSchema:
        budget = await self.repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        if "amount" in params.model_fields_set and params.amount is not None and params.amount < 0:
            raise AmountMustBePositiveError

        if "name" in params.model_fields_set and params.name is not None:
            budget.name = params.name
        if "description" in params.model_fields_set and params.description is not None:
            budget.description = params.description
        if "amount" in params.model_fields_set and params.amount is not None:
            budget.amount = params.amount
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
