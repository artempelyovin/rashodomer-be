from pathlib import Path

import pytest

from domain.models.category import Category
from domain.models.transaction import TransactionType
from infra.repos.file.category import CategoryFileRepo


@pytest.fixture
def repo(tmp_path: Path) -> CategoryFileRepo:
    return CategoryFileRepo(base_dir=tmp_path / "categories")


@pytest.mark.asyncio
async def test_create_and_get_by_id(repo: CategoryFileRepo) -> None:
    category = Category(
        id="c_1",
        name="Groceries",
        user_id="u_1",
        transaction_type=TransactionType.EXPENSE,
    )

    await repo.create(category)
    saved_category = await repo.get_by_id("c_1")

    assert saved_category == category


@pytest.mark.asyncio
async def test_get_by_user_id_without_type(repo: CategoryFileRepo) -> None:
    cat1 = Category(id="c_1", name="Food", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat2 = Category(id="c_2", name="Salary", user_id="u_1", transaction_type=TransactionType.INCOME)
    cat3 = Category(id="c_3", name="Other", user_id="u_2", transaction_type=TransactionType.EXPENSE)

    await repo.create(cat1)
    await repo.create(cat2)
    await repo.create(cat3)

    user1_categories = await repo.get_by_user_id("u_1")

    assert len(user1_categories) == 2
    assert cat1 in user1_categories
    assert cat2 in user1_categories


@pytest.mark.asyncio
async def test_get_by_user_id_with_type(repo: CategoryFileRepo) -> None:
    cat1 = Category(id="c_1", name="Food", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat2 = Category(id="c_2", name="Transport", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat3 = Category(id="c_3", name="Salary", user_id="u_1", transaction_type=TransactionType.INCOME)

    await repo.create(cat1)
    await repo.create(cat2)
    await repo.create(cat3)

    expense_categories = await repo.get_by_user_id("u_1", transaction_type=TransactionType.EXPENSE)

    assert len(expense_categories) == 2
    assert cat1 in expense_categories
    assert cat2 in expense_categories
    assert cat3 not in expense_categories


@pytest.mark.asyncio
async def test_update(repo: CategoryFileRepo) -> None:
    category = Category(id="c_1", name="Old", user_id="u_1")
    await repo.create(category)

    category.name = "New"
    category.transaction_type = TransactionType.TRANSFER
    await repo.update(category)

    updated_category = await repo.get_by_id("c_1")
    assert updated_category is not None
    assert updated_category.name == "New"
    assert updated_category.transaction_type == TransactionType.TRANSFER


@pytest.mark.asyncio
async def test_delete(repo: CategoryFileRepo) -> None:
    category = Category(id="c_1", name="Del", user_id="u_1")
    await repo.create(category)

    await repo.delete("c_1")

    assert await repo.get_by_id("c_1") is None
