from datetime import UTC, datetime

import emoji

from enums import CategoryType
from exceptions import (
    CategoryAccessDeniedError,
    CategoryAlreadyExistsError,
    CategoryNotExistsError,
    EmptyCategoryNameError,
    EmptySearchTextError,
    NotEmojiIconError,
)
from repos.abc import CategoryRepo, Total
from schemas.category import CategorySchema, CreateCategorySchema
from settings import settings
from utils import UnsetValue


class CategoryManager:
    def __init__(self, category_repo: CategoryRepo = settings.category_repo) -> None:
        self.repo = category_repo

    async def create(self, user_id: str, data: CreateCategorySchema) -> CategorySchema:
        if len(data.name) == 0:
            raise EmptyCategoryNameError
        if data.emoji_icon is not None and not emoji.is_emoji(data.emoji_icon):
            raise NotEmojiIconError(emoji_icon=data.emoji_icon)
        total_exist_categories, _ = await self.repo.find_by_name_and_category(
            user_id=user_id, name=data.name, category_type=data.type
        )
        if total_exist_categories != 0:
            raise CategoryAlreadyExistsError(name=data.name, category_type=data.type)
        category = CategorySchema(
            name=data.name,
            description=data.description,
            type=data.type,
            emoji_icon=data.emoji_icon,
            is_archived=False,
            user_id=user_id,
        )
        return await self.repo.add(category)

    async def get(self, user_id: str, category_id: str) -> CategorySchema:
        category = await self.repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        return category

    async def list_(
        self, user_id: str, category_type: CategoryType, *, show_archived: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[CategorySchema]]:
        return await self.repo.list_(
            user_id=user_id, category_type=category_type, show_archived=show_archived, limit=limit, offset=offset
        )

    async def update(
        self,
        user_id: str,
        category_id: str,
        name: str | UnsetValue,
        description: str | UnsetValue,
        category_type: CategoryType | UnsetValue,
        is_archived: bool | UnsetValue,
        emoji_icon: str | None | UnsetValue,
    ) -> CategorySchema:
        category = await self.repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError

        if not isinstance(name, UnsetValue):
            category.name = name
        if not isinstance(description, UnsetValue):
            category.description = description
        if not isinstance(category_type, UnsetValue):
            category.type = category_type
        if not isinstance(is_archived, UnsetValue):
            category.is_archived = is_archived
        if not isinstance(emoji_icon, UnsetValue):
            category.emoji_icon = emoji_icon
        category.updated_at = datetime.now(tz=UTC)
        return await self.repo.update(category)
        # тут логика по изменению бюджетов, при условии смены `category_type`

    async def delete(self, user_id: str, category_id: str) -> CategorySchema:
        category = await self.repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError
        return await self.repo.delete(category_id)

    async def find(
        self, user_id: str, text: str, *, case_sensitive: bool, limit: int | None, offset: int
    ) -> tuple[Total, list[CategorySchema]]:
        if len(text) == 0:
            raise EmptySearchTextError
        return await self.repo.find_by_text(
            user_id=user_id, text=text, case_sensitive=case_sensitive, limit=limit, offset=offset
        )
