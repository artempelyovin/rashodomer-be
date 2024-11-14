from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAlreadyExistsError, UserNotExistsError
from core.services import BudgetService, UserService


class CreateBudgetUseCase:
    def __init__(self, user_service: UserService, budget_service: BudgetService):
        self._user_repo = user_service
        self._budget_repo = budget_service

    async def create(self, name: str, description: str, amount: float, user_id: str) -> Budget:
        user = await self._user_repo.get(user_id)
        if not user:
            raise UserNotExistsError(user_id=user_id)
        if amount < 0:
            raise AmountMustBePositiveError
        exist_budgets = await self._budget_repo.find_by_name(user_id=user_id, name=name)
        if exist_budgets:
            raise BudgetAlreadyExistsError(name=name)
        return await self._budget_repo.create(name=name, description=description, amount=amount, user_id=user_id)
