# ruff: noqa: S311
import random
from unittest.mock import Mock

import pytest

from core.entities import Category
from core.enums import CategoryType
from core.exceptions import CategoryAlreadyExistsError, EmptyCategoryNameError, NotEmojiIconError
from core.services import CategoryService, EmojiService
from core.use_cases.category.create import CreateCategoryUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryService)
    category_service.find.return_value = (0, [])
    category_service.create.return_value = fake_category
    emoji_service = Mock(spec=EmojiService)

    use_case = CreateCategoryUseCase(category_service, emoji_service)

    created_category = await use_case.create(
        user_id=str(fake.uuid4()),
        name=fake.word(),
        description=fake.sentence(),
        category_type=random.choice(list(CategoryType)),
        emoji_icon=random.choice([None, fake.emoji()]),
    )

    assert created_category == fake_category


async def test_empty_category_name() -> None:
    category_service = Mock(spec=CategoryService)
    emoji_service = Mock(spec=EmojiService)

    use_case = CreateCategoryUseCase(category_service, emoji_service)

    with pytest.raises(EmptyCategoryNameError):
        await use_case.create(
            user_id=str(fake.uuid4()),
            name="",  # empty name
            description=fake.sentence(),
            category_type=random.choice(list(CategoryType)),
            emoji_icon=random.choice([None, fake.emoji()]),
        )


@pytest.mark.parametrize("bad_emoji_icon", ["🍿s", "not emodj", "s", ""])
async def test_not_emoji_icon(bad_emoji_icon: str) -> None:
    category_service = Mock(spec=CategoryService)
    emoji_service = Mock(spec=EmojiService)
    emoji_service.is_emoji.return_value = False

    use_case = CreateCategoryUseCase(category_service, emoji_service)

    with pytest.raises(NotEmojiIconError):
        await use_case.create(
            user_id=str(fake.uuid4()),
            name=fake.word(),
            description=fake.sentence(),
            category_type=random.choice(list(CategoryType)),
            emoji_icon=bad_emoji_icon,  # not emoji icon
        )


async def test_category_already_exists(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryService)
    category_service.find.return_value = (1, [fake_category])
    emoji_service = Mock(spec=EmojiService)

    use_case = CreateCategoryUseCase(category_service, emoji_service)

    with pytest.raises(CategoryAlreadyExistsError):
        await use_case.create(
            user_id=str(fake.uuid4()),
            name=fake.word(),
            description=fake.sentence(),
            category_type=random.choice(list(CategoryType)),
            emoji_icon=random.choice([None, fake.emoji()]),
        )
