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
from models import CategorySchema
from repos.abc import CategoryRepo, Total
from settings import settings


class CategoryManager:
    def __init__(self, category_repo: CategoryRepo = settings.category_repo) -> None:
        self.repo = category_repo

    async def create(
        self,
        user_id: str,
        name: str,
        category_type: CategoryType,
        description: str | None = "",
        emoji_icon: str | None = None,
    ) -> CategorySchema:
        if len(name) == 0:
            raise EmptyCategoryNameError
        if emoji_icon is not None and not emoji.is_emoji(emoji_icon):
            raise NotEmojiIconError(emoji_icon=emoji_icon)
        total_exist_categories, _ = await self.repo.find_by_name_and_category(
            user_id=user_id, name=name, category_type=category_type
        )
        if total_exist_categories != 0:
            raise CategoryAlreadyExistsError(name=name, category_type=category_type)
        category = CategorySchema(
            name=name,
            description=description,
            type=category_type,
            emoji_icon=emoji_icon,
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
        self,
        user_id: str,
        *,
        category_type: CategoryType | None = None,
        show_archived: bool | None = False,
        limit: int | None,
        offset: int,
    ) -> tuple[Total, list[CategorySchema]]:
        return await self.repo.list_(
            user_id=user_id, category_type=category_type, show_archived=show_archived, limit=limit, offset=offset
        )

    async def update(
        self,
        user_id: str,
        category_id: str,
        name: str,
        description: str,
        category_type: CategoryType,
        is_archived: bool,
        emoji_icon: str | None,
    ) -> CategorySchema:
        category = await self.repo.get(category_id)
        if not category:
            raise CategoryNotExistsError(category_id=category_id)
        if category.user_id != user_id:
            raise CategoryAccessDeniedError

        category.name = name
        category.description = description
        category.type = category_type
        category.is_archived = is_archived
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
