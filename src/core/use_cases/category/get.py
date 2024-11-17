from core.entities import Category
from core.exceptions import CategoryAccessDeniedError, CategoryNotExistsError
from core.services import CategoryService


class GetCategoryUseCase:
    def __init__(self, category_service: CategoryService) -> None:
        self._category_repo = category_service

    async def get(self, user_id: str, category_id: str) -> Category:
        category = await self._category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        return category
