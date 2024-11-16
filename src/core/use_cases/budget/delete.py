from core.entities import Budget
from core.exceptions import BudgetAccessDeniedError, BudgetNotExistsError
from core.services import BudgetService


class DeleteBudgetUseCase:
    def __init__(self, budget_service: BudgetService) -> None:
        self._budget_repo = budget_service

    async def delete(self, user_id: str, budget_id: str) -> Budget:
        budget = await self._budget_repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return await self._budget_repo.delete(budget_id)
