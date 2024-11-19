from unittest.mock import AsyncMock

import pytest

from core.entities import Category
from core.exceptions import CategoryAccessDeniedError, CategoryNotExistsError
from core.repos import CategoryRepository
from core.use_cases.category.get import GetCategoryUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_category: Category) -> None:
    category_service = AsyncMock(spec=CategoryRepository)
    category_service.get.return_value = fake_category
    use_case = GetCategoryUseCase(category_service)

    category = await use_case.get(user_id=fake_category.user_id, category_id=fake_category.id)

    assert category == fake_category
    category_service.get.assert_called_once_with(fake_category.id)


async def test_category_not_exists() -> None:
    category_service = AsyncMock(spec=CategoryRepository)
    category_service.get.return_value = None
    use_case = GetCategoryUseCase(category_service)

    with pytest.raises(CategoryNotExistsError):
        await use_case.get(user_id=str(fake.uuid4()), category_id=str(fake.uuid4()))


async def test_category_access_denied(fake_category: Category) -> None:
    category_service = AsyncMock(spec=CategoryRepository)
    category_service.get.return_value = fake_category
    use_case = GetCategoryUseCase(category_service)

    with pytest.raises(CategoryAccessDeniedError):
        await use_case.get(
            user_id=str(fake.uuid4()),  # another user
            category_id=fake_category.id,
        )
