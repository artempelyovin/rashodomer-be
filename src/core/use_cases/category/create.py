from core.entities import Category
from core.enums import TransactionType
from core.exceptions import CategoryAlreadyExistsError, EmptyCategoryNameError, NotEmojiIconError
from core.repos import CategoryRepository
from core.services import EmojiService


class CreateCategoryUseCase:
    def __init__(self, category_service: CategoryRepository, emoji_service: EmojiService) -> None:
        self._category_service = category_service
        self._emoji_service = emoji_service

    async def create(
        self, user_id: str, name: str, description: str, transaction_type: TransactionType, emoji_icon: str | None
    ) -> Category:
        if len(name) == 0:
            raise EmptyCategoryNameError
        if emoji_icon is not None and not self._emoji_service.is_emoji(emoji_icon):
            raise NotEmojiIconError(emoji_icon=emoji_icon)
        total_exist_categories, _ = await self._category_service.list_(
            user_id=user_id, transaction_type=transaction_type, name=name
        )
        if total_exist_categories != 0:
            raise CategoryAlreadyExistsError(name=name, transaction_type=transaction_type)
        category = Category(
            user_id=user_id, name=name, description=description, type=transaction_type, emoji_icon=emoji_icon
        )
        return await self._category_service.create(category)
