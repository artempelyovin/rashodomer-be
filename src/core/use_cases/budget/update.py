from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAccessDeniedError, BudgetNotExistsError
from core.services import BudgetService


class UpdateBudgetUseCase:
    def __init__(self, budget_service: BudgetService) -> None:
        self._budget_repo = budget_service

    async def update(
        self, user_id: str, budget_id: str, name: str | None, description: str | None, amount: float | None
    ) -> Budget:
        budget = await self._budget_repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        if amount and amount < 0:
            raise AmountMustBePositiveError
        return await self._budget_repo.update_budget(
            budget_id=budget_id, name=name, description=description, amount=amount
        )
