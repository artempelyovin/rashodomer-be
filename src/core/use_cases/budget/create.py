from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAlreadyExistsError
from core.repos import BudgetRepository


class CreateBudgetUseCase:
    def __init__(self, budget_service: BudgetRepository) -> None:
        self._budget_repo = budget_service

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        if amount < 0:
            raise AmountMustBePositiveError
        _, exist_budgets = await self._budget_repo.find_by_name(user_id=user_id, name=name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        return await self._budget_repo.create(name=name, description=description, amount=amount, user_id=user_id)
