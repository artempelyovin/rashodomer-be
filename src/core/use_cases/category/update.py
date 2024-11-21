from core.entities import Category
from core.enums import TransactionType
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
        transaction_type: TransactionType | UnsetValue,
        is_archived: bool | UnsetValue,
        emoji_icon: str | None | UnsetValue,
    ) -> Category:
        category = await self._category_repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        if not isinstance(name, UnsetValue):
            category.name = name
        if not isinstance(description, UnsetValue):
            category.description = description
        if not isinstance(transaction_type, UnsetValue):
            category.type = transaction_type
        if not isinstance(is_archived, UnsetValue):
            category.is_archived = is_archived
        if not isinstance(emoji_icon, UnsetValue):
            category.emoji_icon = emoji_icon
        return await self._category_repo.update(category)
        # тут логика по изменению бюджетов, при условии смены `transaction_type`
