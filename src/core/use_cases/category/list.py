from core.entities import Category
from core.enums import TransactionType
from core.repos import CategoryRepository
from core.services import Total


class ListCategoryUseCase:
    def __init__(self, category_service: CategoryRepository) -> None:
        self._category_service = category_service

    async def list(
        self, user_id: str, transaction_type: TransactionType, *, show_archived: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[Category]]:
        return await self._category_service.list_(
            user_id=user_id, transaction_type=transaction_type, show_archived=show_archived, limit=limit, offset=offset
        )
