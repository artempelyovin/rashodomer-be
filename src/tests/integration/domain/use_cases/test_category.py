import pytest

from domain.errors import CategoryNotFoundError, EmptyNameError
from domain.models.transaction import TransactionType
from domain.use_cases.category import (
    CreateCategory,
    DeleteCategory,
    GetCategory,
    ListCategories,
    UpdateCategory,
)


@pytest.mark.asyncio
async def test_create_category_success(create_category: CreateCategory) -> None:
    category = await create_category.execute(
        name="Groceries",
        user_id="user-123",
        transaction_type=TransactionType.EXPENSE,
        description="Food expenses",
    )

    assert category.id is not None
    assert category.name == "Groceries"
    assert category.user_id == "user-123"
    assert category.transaction_type == TransactionType.EXPENSE
    assert category.description == "Food expenses"
    assert category.created_at is not None
    assert category.updated_at is not None


@pytest.mark.asyncio
async def test_create_category_without_type(create_category: CreateCategory) -> None:
    category = await create_category.execute(
        name="General",
        user_id="user-123",
    )
    assert category.transaction_type is None
    assert category.name == "General"


@pytest.mark.asyncio
async def test_create_category_empty_name(create_category: CreateCategory) -> None:
    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await create_category.execute(name="", user_id="user-123")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await create_category.execute(name="   ", user_id="user-123")


@pytest.mark.asyncio
async def test_get_category_success(get_category: GetCategory, create_category: CreateCategory) -> None:
    created = await create_category.execute(name="Test Category", user_id="user-123")
    fetched = await get_category.execute(created.id)

    assert fetched == created


@pytest.mark.asyncio
async def test_get_category_not_found(get_category: GetCategory) -> None:
    with pytest.raises(CategoryNotFoundError, match="Category with id 'missing-id' not found"):
        await get_category.execute("missing-id")


@pytest.mark.asyncio
async def test_list_categories_empty(list_categories: ListCategories) -> None:
    categories = await list_categories.execute("user-empty")
    assert categories == []


@pytest.mark.asyncio
async def test_list_categories_multiple(list_categories: ListCategories, create_category: CreateCategory) -> None:
    user_id = "user-multi"
    cat1 = await create_category.execute(name="Food", user_id=user_id, transaction_type=TransactionType.EXPENSE)
    cat2 = await create_category.execute(name="Salary", user_id=user_id, transaction_type=TransactionType.INCOME)
    # Another user's category should not appear
    await create_category.execute(name="Other", user_id="other-user")

    categories = await list_categories.execute(user_id)

    assert len(categories) == 2
    assert cat1 in categories
    assert cat2 in categories


@pytest.mark.asyncio
async def test_list_categories_filtered_by_type(
    list_categories: ListCategories, create_category: CreateCategory
) -> None:
    user_id = "user-filter"
    await create_category.execute(name="Food", user_id=user_id, transaction_type=TransactionType.EXPENSE)
    await create_category.execute(name="Transport", user_id=user_id, transaction_type=TransactionType.EXPENSE)
    await create_category.execute(name="Salary", user_id=user_id, transaction_type=TransactionType.INCOME)

    expense_cats = await list_categories.execute(user_id, transaction_type=TransactionType.EXPENSE)
    income_cats = await list_categories.execute(user_id, transaction_type=TransactionType.INCOME)

    assert len(expense_cats) == 2
    assert len(income_cats) == 1
    assert all(c.transaction_type == TransactionType.EXPENSE for c in expense_cats)


@pytest.mark.asyncio
async def test_update_category_full_update(update_category: UpdateCategory, create_category: CreateCategory) -> None:
    category = await create_category.execute(
        name="Old Name",
        user_id="user-123",
        transaction_type=TransactionType.EXPENSE,
        description="Old description",
    )

    updated = await update_category.execute(
        category_id=category.id,
        name="New Name",
        transaction_type=TransactionType.INCOME,
        description="New description",
    )

    assert updated.id == category.id
    assert updated.name == "New Name"
    assert updated.transaction_type == TransactionType.INCOME
    assert updated.description == "New description"
    assert updated.user_id == category.user_id
    # updated_at должен измениться
    assert updated.updated_at > category.updated_at


@pytest.mark.asyncio
async def test_update_category_partial(update_category: UpdateCategory, create_category: CreateCategory) -> None:
    category = await create_category.execute(
        name="Original", user_id="user-123", transaction_type=TransactionType.EXPENSE, description="Desc"
    )

    updated = await update_category.execute(category_id=category.id, name="Changed Name")

    assert updated.name == "Changed Name"
    assert updated.transaction_type == TransactionType.EXPENSE  # unchanged
    assert updated.description == "Desc"  # unchanged


@pytest.mark.asyncio
async def test_update_category_set_description_to_none(
    update_category: UpdateCategory, create_category: CreateCategory
) -> None:
    category = await create_category.execute(name="Budget", user_id="user-123", description="Some desc")

    # Update description to None explicitly
    updated = await update_category.execute(category_id=category.id, description=None)

    assert updated.description is None

    # Ensure that using UNSET leaves description unchanged
    updated2 = await update_category.execute(category_id=category.id, name="Renamed")
    assert updated2.description is None  # still None


@pytest.mark.asyncio
async def test_update_category_empty_name(update_category: UpdateCategory, create_category: CreateCategory) -> None:
    category = await create_category.execute(name="Budget", user_id="user-123")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await update_category.execute(category_id=category.id, name="")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await update_category.execute(category_id=category.id, name="   ")


@pytest.mark.asyncio
async def test_update_category_not_found(update_category: UpdateCategory) -> None:
    with pytest.raises(CategoryNotFoundError, match="Category with id 'missing' not found"):
        await update_category.execute(category_id="missing", name="New Name")


@pytest.mark.asyncio
async def test_delete_category_success(
    delete_category: DeleteCategory, create_category: CreateCategory, get_category: GetCategory
) -> None:
    category = await create_category.execute(name="ToDelete", user_id="user-123")
    await delete_category.execute(category.id)

    with pytest.raises(CategoryNotFoundError):
        await get_category.execute(category.id)


@pytest.mark.asyncio
async def test_delete_category_not_found(delete_category: DeleteCategory) -> None:
    with pytest.raises(CategoryNotFoundError, match="Category with id 'missing' not found"):
        await delete_category.execute("missing")
