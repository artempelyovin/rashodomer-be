from core.entities import Budget
from core.repos import BudgetRepository
from core.services import Total


class ListBudgetUseCase:
    def __init__(self, budget_service: BudgetRepository) -> None:
        self._budget_repo = budget_service

    async def list(self, user_id: str, limit: int | None, offset: int) -> tuple[Total, list[Budget]]:
        return await self._budget_repo.list_(user_id=user_id, limit=limit, offset=offset)
