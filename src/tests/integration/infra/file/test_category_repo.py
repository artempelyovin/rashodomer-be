import pytest

from domain.models.category import Category
from domain.models.transaction import TransactionType
from infra.repos.file.category import CategoryFileRepo


@pytest.mark.asyncio
async def test_create_and_get_by_id(category_repo: CategoryFileRepo) -> None:
    category = Category(
        id="c_1",
        name="Groceries",
        user_id="u_1",
        transaction_type=TransactionType.EXPENSE,
    )

    await category_repo.create(category)
    saved_category = await category_repo.get_by_id("c_1")

    assert saved_category == category


@pytest.mark.asyncio
async def test_get_by_user_id_without_type(category_repo: CategoryFileRepo) -> None:
    cat1 = Category(id="c_1", name="Food", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat2 = Category(id="c_2", name="Salary", user_id="u_1", transaction_type=TransactionType.INCOME)
    cat3 = Category(id="c_3", name="Other", user_id="u_2", transaction_type=TransactionType.EXPENSE)

    await category_repo.create(cat1)
    await category_repo.create(cat2)
    await category_repo.create(cat3)

    user1_categories = await category_repo.get_by_user_id("u_1")

    assert len(user1_categories) == 2
    assert cat1 in user1_categories
    assert cat2 in user1_categories


@pytest.mark.asyncio
async def test_get_by_user_id_with_type(category_repo: CategoryFileRepo) -> None:
    cat1 = Category(id="c_1", name="Food", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat2 = Category(id="c_2", name="Transport", user_id="u_1", transaction_type=TransactionType.EXPENSE)
    cat3 = Category(id="c_3", name="Salary", user_id="u_1", transaction_type=TransactionType.INCOME)

    await category_repo.create(cat1)
    await category_repo.create(cat2)
    await category_repo.create(cat3)

    expense_categories = await category_repo.get_by_user_id("u_1", transaction_type=TransactionType.EXPENSE)

    assert len(expense_categories) == 2
    assert cat1 in expense_categories
    assert cat2 in expense_categories
    assert cat3 not in expense_categories


@pytest.mark.asyncio
async def test_update(category_repo: CategoryFileRepo) -> None:
    category = Category(id="c_1", name="Old", user_id="u_1")
    await category_repo.create(category)

    category.name = "New"
    category.transaction_type = TransactionType.TRANSFER
    await category_repo.update(category)

    updated_category = await category_repo.get_by_id("c_1")
    assert updated_category is not None
    assert updated_category.name == "New"
    assert updated_category.transaction_type == TransactionType.TRANSFER


@pytest.mark.asyncio
async def test_delete(category_repo: CategoryFileRepo) -> None:
    category = Category(id="c_1", name="Del", user_id="u_1")
    await category_repo.create(category)

    await category_repo.delete("c_1")

    assert await category_repo.get_by_id("c_1") is None
