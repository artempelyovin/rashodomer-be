from core.entities import Budget
from core.exceptions import EmptyInputError
from core.services import BudgetService, Total


class FindBudgetUseCase:
    def __init__(self, budget_service: BudgetService) -> None:
        self._budget_repo = budget_service

    async def find(self, user_id: str, text: str, limit: int | None, offset: int) -> tuple[Total, list[Budget]]:
        if len(text) == 0:
            raise EmptyInputError
        return await self._budget_repo.find_by_text(user_id=user_id, text=text, limit=limit, offset=offset)
