from core.entities import Category
from core.exceptions import EmptySearchTextError
from core.services import Total
from core.repos import CategoryRepository


class FindCategoryUseCase:
    def __init__(self, category_service: CategoryRepository) -> None:
        self._category_repo = category_service

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[Category]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self._category_repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
