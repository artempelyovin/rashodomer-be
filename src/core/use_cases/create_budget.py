from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAlreadyExistsError
from core.services import BudgetService


class CreateBudgetUseCase:
    def __init__(self, budget_service: BudgetService) -> None:
        self._budget_repo = budget_service

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        if amount < 0:
            raise AmountMustBePositiveError
        exist_budgets = await self._budget_repo.find_by_name(user_id=user_id, name=name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        return await self._budget_repo.create(name=name, description=description, amount=amount, user_id=user_id)
