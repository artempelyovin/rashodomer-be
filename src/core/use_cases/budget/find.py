from core.entities import Budget
from core.exceptions import EmptySearchTextError
from core.repos import BudgetRepository
from core.services import Total


class FindBudgetUseCase:
    def __init__(self, budget_service: BudgetRepository) -> None:
        self._budget_repo = budget_service

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[Budget]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self._budget_repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
