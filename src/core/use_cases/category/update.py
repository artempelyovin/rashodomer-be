from core.entities import Category
from core.enums import CategoryType
from core.exceptions import CategoryAccessDeniedError, CategoryNotExistsError
from core.repos import CategoryRepository
from core.utils import UnsetValue


class UpdateCategoryUseCase:
    def __init__(self, category_service: CategoryRepository) -> None:
        self._category_repo = category_service

    async def update(
        self,
        user_id: str,
        category_id: str,
        name: str | UnsetValue,
        description: str | UnsetValue,
        category_type: CategoryType | UnsetValue,
        is_archived: bool | UnsetValue,
        emoji_icon: str | None | UnsetValue,
    ) -> Category:
        category = await self._category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        return await self._category_repo.update_category(
            category_id=category_id,
            name=name,
            description=description,
            category_type=category_type,
            is_archived=is_archived,
            emoji_icon=emoji_icon,
        )
        # тут логика по изменению бюджетов, при условии смены `category_type`
