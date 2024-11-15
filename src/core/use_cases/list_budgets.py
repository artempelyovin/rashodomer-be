from core.entities import Budget
from core.exceptions import UserNotExistsError
from core.services import BudgetService, UserService


class ListBudgetUseCase:
    def __init__(self, user_service: UserService, budget_service: BudgetService):
        self._user_repo = user_service
        self._budget_repo = budget_service

    async def list(self, user_id: str) -> list[Budget]:
        user = await self._user_repo.get(user_id)
        if not user:
            raise UserNotExistsError(user_id=user_id)
        return await self._budget_repo.find(user_id=user_id)
