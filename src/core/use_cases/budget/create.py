from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAlreadyExistsError
from core.repos import BudgetRepository


class CreateBudgetUseCase:
    def __init__(self, budget_service: BudgetRepository) -> None:
        self._budget_repo = budget_service

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        if amount < 0:
            raise AmountMustBePositiveError
        total_exist_budgets, _ = await self._budget_repo.list_(user_id=user_id, name=name)
        if total_exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        budget = Budget(name=name, description=description, amount=amount, user_id=user_id)
        return await self._budget_repo.create(budget)
