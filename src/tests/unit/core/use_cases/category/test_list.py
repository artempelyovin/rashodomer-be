# ruff: noqa: S311
import random
from unittest.mock import Mock

from core.entities import Category
from core.enums import TransactionType
from core.services import CategoryService
from core.use_cases.category.list import ListCategoryUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_category: Category) -> None:
    category_service = Mock(spec=CategoryService)
    expected_categories = [fake_category, fake_category]
    expected_total = len(expected_categories)
    category_service.list_.return_value = (expected_total, expected_categories)
    use_case = ListCategoryUseCase(category_service)

    total, categories = await use_case.list(
        user_id=fake_category.user_id,
        transaction_type=random.choice(list(TransactionType)),
        show_archived=fake.pybool(),
        limit=None,
        offset=0,
    )

    assert total == expected_total
    assert len(categories) == len(expected_categories)
    for category, expected_category in zip(categories, expected_categories, strict=True):
        assert category == expected_category
