from unittest.mock import Mock

import pytest

from core.entities import Category
from core.enums import TransactionType
from core.exceptions import CategoryAccessDeniedError, CategoryNotExistsError
from core.repos import CategoryRepository
from core.use_cases.category.update import UpdateCategoryUseCase
from core.utils import UNSET
from tests.unit.core.conftest import fake


async def test_success(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = fake_category
    updated_category = Category(
        id=fake_category.id,
        user_id=fake_category.user_id,
        name=fake.word(),
        description=fake.sentence(),
        type=fake.random_element(list(TransactionType)),
        is_archived=fake.pybool(),
        emoji_icon=fake.emoji(),
    )
    category_service.update.return_value = updated_category
    use_case = UpdateCategoryUseCase(category_service)

    updated_category = await use_case.update(
        user_id=fake_category.user_id,
        category_id=fake_category.id,
        name=updated_category.name,
        description=updated_category.description,
        transaction_type=updated_category.type,
        is_archived=updated_category.is_archived,
        emoji_icon=updated_category.emoji_icon,
    )

    # unchanged
    assert updated_category.id == fake_category.id
    assert updated_category.user_id == fake_category.user_id
    # changed
    assert updated_category != fake_category


async def test_category_not_exists(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = None
    use_case = UpdateCategoryUseCase(category_service)

    with pytest.raises(CategoryNotExistsError):
        await use_case.update(
            user_id=fake_category.user_id,
            category_id=fake_category.id,
            name=UNSET,
            description=UNSET,
            transaction_type=UNSET,
            is_archived=UNSET,
            emoji_icon=UNSET,
        )


async def test_category_access_denied(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = fake_category
    use_case = UpdateCategoryUseCase(category_service)

    with pytest.raises(CategoryAccessDeniedError):
        await use_case.update(
            user_id=str(fake.uuid4()),  # another user
            category_id=fake_category.id,
            name=UNSET,
            description=UNSET,
            transaction_type=UNSET,
            is_archived=UNSET,
            emoji_icon=UNSET,
        )
