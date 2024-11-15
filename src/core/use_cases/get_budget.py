from core.entities import Budget
from core.exceptions import BudgetAccessDeniedError, BudgetNotExistsError, UserNotExistsError
from core.services import BudgetService, UserService


class GetBudgetUseCase:
    def __init__(self, user_service: UserService, budget_service: BudgetService):
        self._user_repo = user_service
        self._budget_repo = budget_service

    async def get(self, user_id: str, budget_id: str) -> Budget:
        user = await self._user_repo.get(user_id)
        if not user:
            raise UserNotExistsError(user_id=user_id)
        budget = await self._budget_repo.get(budget_id)
        if not budget:
            raise BudgetNotExistsError(budget_id=budget_id)
        if budget.user_id != user_id:
            raise BudgetAccessDeniedError
        return budget
