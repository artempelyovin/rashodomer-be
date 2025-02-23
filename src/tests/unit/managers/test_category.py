# ruff: noqa: S311
import random
from unittest.mock import Mock

import pytest

from enums import CategoryType
from exceptions import (
    CategoryAccessDeniedError,
    CategoryAlreadyExistsError,
    CategoryNotExistsError,
    EmptyCategoryNameError,
    EmptySearchTextError,
    NotEmojiIconError,
)
from managers.category import CategoryManager
from repos.abc import CategoryRepo
from schemas.category import CategorySchema, CreateCategorySchema
from tests.unit.conftest import fake
from utils import UNSET


@pytest.fixture
def category_repo():
    return Mock(spec=CategoryRepo)


class TestCategoryManagerCreate:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.find_by_name_and_category.return_value = (0, [])
        category_repo.add.return_value = fake_category
        manager = CategoryManager(category_repo=category_repo)

        created_category = await manager.create(
            user_id=str(fake.uuid4()),
            data=CreateCategorySchema(
                name=fake.word(),
                description=fake.sentence(),
                type=random.choice(list(CategoryType)),
                emoji_icon=random.choice([None, fake.emoji()]),
            ),
        )

        assert created_category == fake_category

    async def test_empty_category_name(self, category_repo) -> None:
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(EmptyCategoryNameError):
            await manager.create(
                user_id=str(fake.uuid4()),
                data=CreateCategorySchema(
                    name="",  # <-- empty name
                    description=fake.sentence(),
                    type=random.choice(list(CategoryType)),
                    emoji_icon=random.choice([None, fake.emoji()]),
                ),
            )

    @pytest.mark.parametrize("bad_emoji_icon", ["🍿s", "not emodj", "s", ""])
    async def test_not_emoji_icon(self, category_repo, bad_emoji_icon: str) -> None:
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(NotEmojiIconError):
            await manager.create(
                user_id=str(fake.uuid4()),
                data=CreateCategorySchema(
                    name=fake.word(),
                    description=fake.sentence(),
                    type=random.choice(list(CategoryType)),
                    emoji_icon=bad_emoji_icon,  # <-- not emoji icon
                ),
            )

    async def test_category_already_exists(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.find_by_name_and_category.return_value = (1, [fake_category])
        manager = CategoryManager(category_repo)

        with pytest.raises(CategoryAlreadyExistsError):
            await manager.create(
                user_id=str(fake.uuid4()),
                data=CreateCategorySchema(
                    name=fake.word(),
                    description=fake.sentence(),
                    type=random.choice(list(CategoryType)),
                    emoji_icon=random.choice([None, fake.emoji()]),
                ),
            )


class TestCategoryManagerGet:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category
        manager = CategoryManager(category_repo=category_repo)

        category = await manager.get(user_id=fake_category.user_id, category_id=fake_category.id)

        assert category == fake_category
        category_repo.get.assert_called_once_with(fake_category.id)

    async def test_category_not_exists(self, category_repo) -> None:
        category_repo.get.return_value = None
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryNotExistsError):
            await manager.get(user_id=str(fake.uuid4()), category_id=str(fake.uuid4()))

    async def test_category_access_denied(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryAccessDeniedError):
            await manager.get(
                user_id=str(fake.uuid4()),  # another user
                category_id=fake_category.id,
            )


class TestCategoryManagerList:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        expected_categories = [fake_category, fake_category]
        expected_total = len(expected_categories)
        category_repo.list_.return_value = (expected_total, expected_categories)
        manager = CategoryManager(category_repo=category_repo)

        total, categories = await manager.list_(
            user_id=fake_category.user_id,
            category_type=random.choice(list(CategoryType)),
            show_archived=fake.pybool(),
            limit=None,
            offset=0,
        )

        assert total == expected_total
        assert len(categories) == len(expected_categories)
        for category, expected_category in zip(categories, expected_categories, strict=True):
            assert category == expected_category


class TestCategoryManagerUpdate:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category
        updated_category = CategorySchema(
            id=fake_category.id,
            user_id=fake_category.user_id,
            name=fake.word(),
            description=fake.sentence(),
            type=fake.random_element(list(CategoryType)),
            is_archived=fake.pybool(),
            emoji_icon=fake.emoji(),
        )
        category_repo.update_category.return_value = updated_category
        manager = CategoryManager(category_repo=category_repo)

        updated_category = await manager.update(
            user_id=fake_category.user_id,
            category_id=fake_category.id,
            name=updated_category.name,
            description=updated_category.description,
            category_type=updated_category.type,
            is_archived=updated_category.is_archived,
            emoji_icon=updated_category.emoji_icon,
        )

        # unchanged
        assert updated_category.id == fake_category.id
        assert updated_category.user_id == fake_category.user_id
        # changed
        assert updated_category != fake_category

    async def test_category_not_exists(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = None
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryNotExistsError):
            await manager.update(
                user_id=fake_category.user_id,
                category_id=fake_category.id,
                name=UNSET,
                description=UNSET,
                category_type=UNSET,
                is_archived=UNSET,
                emoji_icon=UNSET,
            )

    async def test_category_access_denied(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryAccessDeniedError):
            await manager.update(
                user_id=str(fake.uuid4()),  # another user
                category_id=fake_category.id,
                name=UNSET,
                description=UNSET,
                category_type=UNSET,
                is_archived=UNSET,
                emoji_icon=UNSET,
            )


class TestCategoryManagerDelete:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category
        category_repo.delete.return_value = fake_category
        manager = CategoryManager(category_repo=category_repo)

        deleted_category = await manager.delete(user_id=fake_category.user_id, category_id=fake_category.id)

        assert deleted_category == fake_category

    async def test_category_not_exists(self, category_repo) -> None:
        category_repo.get.return_value = None

        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryNotExistsError):
            await manager.delete(user_id=str(fake.uuid4()), category_id=str(fake.uuid4()))

    async def test_category_access_denied(self, category_repo, fake_category: CategorySchema) -> None:
        category_repo.get.return_value = fake_category

        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(CategoryAccessDeniedError):
            await manager.delete(
                user_id=str(fake.uuid4()),  # <-- another user
                category_id=fake_category.id,
            )


class TestCategoryManagerFind:
    async def test_success(self, category_repo, fake_category: CategorySchema) -> None:
        categories = [fake_category]
        total = len(categories)
        category_repo.find_by_text.return_value = (total, categories)
        manager = CategoryManager(category_repo=category_repo)

        result_total, result_categories = await manager.find(
            user_id=str(fake.uuid4()),
            text="наличные",
            case_sensitive=fake.pybool(),
            limit=fake.random_element([None, fake.pyint()]),
            offset=fake.pyint(),
        )

        assert result_total == total
        assert len(result_categories) == len(categories)
        for category, expected_category in zip(result_categories, categories, strict=True):
            assert category == expected_category

    async def test_empty_category_text(self, category_repo) -> None:
        manager = CategoryManager(category_repo=category_repo)

        with pytest.raises(EmptySearchTextError):
            await manager.find(
                user_id=str(fake.uuid4()),
                text="",
                case_sensitive=fake.pybool(),
                limit=fake.random_element([None, fake.pyint()]),
                offset=fake.pyint(),
            )
