from unittest.mock import Mock

import pytest

from core.entities import Category
from core.exceptions import EmptySearchTextError
from core.services import CategoryService
from core.use_cases.category.find import FindCategoryUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryService)
    categories = [fake_category]
    total = len(categories)
    category_service.find_by_text.return_value = (total, categories)
    use_case = FindCategoryUseCase(category_service)

    result_total, result_categories = await use_case.find(
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


async def test_empty_category_text() -> None:
    category_service = Mock(spec=CategoryService)
    use_case = FindCategoryUseCase(category_service)

    with pytest.raises(EmptySearchTextError):
        await use_case.find(
            user_id=str(fake.uuid4()),
            text="",
            case_sensitive=fake.pybool(),
            limit=fake.random_element([None, fake.pyint()]),
            offset=fake.pyint(),
        )
