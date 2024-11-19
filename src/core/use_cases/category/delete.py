from core.entities import Category
from core.exceptions import CategoryAccessDeniedError, CategoryNotExistsError
from core.repos import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_service: CategoryRepository) -> None:
        self._category_repo = category_service

    async def delete(self, user_id: str, category_id: str) -> Category:
        category = await self._category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        return await self._category_repo.delete(category_id)
