from core.entities import Budget
from core.services import BudgetService, Total


class ListBudgetUseCase:
    def __init__(self, budget_service: BudgetService) -> None:
        self._budget_repo = budget_service

    async def list(self, user_id: str, limit: int | None, offset: int) -> tuple[Total, list[Budget]]:
        return await self._budget_repo.find(user_id=user_id, limit=limit, offset=offset)
