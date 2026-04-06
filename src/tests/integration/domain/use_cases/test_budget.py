from decimal import Decimal

import pytest

from domain.errors import BudgetNotFoundError, EmptyNameError, NegativeBalanceError
from domain.use_cases.budget import CreateBudget, DeleteBudget, GetBudget, ListBudgets, UpdateBudget


@pytest.mark.asyncio
async def test_create_budget_success(create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(
        name="Monthly Budget",
        balance=Decimal("1500.00"),
        user_id="user-123",
        description="Personal monthly expenses",
    )

    assert budget.id is not None
    assert budget.name == "Monthly Budget"
    assert budget.balance == Decimal("1500.00")
    assert budget.user_id == "user-123"
    assert budget.description == "Personal monthly expenses"
    assert budget.created_at is not None
    assert budget.updated_at is not None


@pytest.mark.asyncio
async def test_create_budget_empty_name(create_budget: CreateBudget) -> None:
    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await create_budget.execute(name="", balance=Decimal(100), user_id="user-123")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await create_budget.execute(name="   ", balance=Decimal(100), user_id="user-123")


@pytest.mark.asyncio
async def test_create_budget_negative_balance(create_budget: CreateBudget) -> None:
    with pytest.raises(NegativeBalanceError, match="Balance cannot be negative: -50"):
        await create_budget.execute(name="Budget", balance=Decimal(-50), user_id="user-123")


@pytest.mark.asyncio
async def test_get_budget_success(get_budget: GetBudget, create_budget: CreateBudget) -> None:
    created = await create_budget.execute(name="Test", balance=Decimal(200), user_id="user-123")
    fetched = await get_budget.execute(created.id)

    assert fetched == created


@pytest.mark.asyncio
async def test_get_budget_not_found(get_budget: GetBudget) -> None:
    with pytest.raises(BudgetNotFoundError, match="Budget with id 'missing-id' not found"):
        await get_budget.execute("missing-id")


@pytest.mark.asyncio
async def test_list_budgets_empty(list_budgets: ListBudgets) -> None:
    budgets = await list_budgets.execute("user-empty")
    assert budgets == []


@pytest.mark.asyncio
async def test_list_budgets_multiple(list_budgets: ListBudgets, create_budget: CreateBudget) -> None:
    user_id = "user-multi"
    budget1 = await create_budget.execute(name="Budget A", balance=Decimal(100), user_id=user_id)
    budget2 = await create_budget.execute(name="Budget B", balance=Decimal(200), user_id=user_id)
    # Another user's budget should not appear
    await create_budget.execute(name="Other", balance=Decimal(300), user_id="other-user")

    budgets = await list_budgets.execute(user_id)

    assert len(budgets) == 2
    assert budget1 in budgets
    assert budget2 in budgets


@pytest.mark.asyncio
async def test_update_budget_full_update(update_budget: UpdateBudget, create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(
        name="Old Name",
        balance=Decimal("100.00"),
        user_id="user-123",
        description="Old description",
    )

    updated = await update_budget.execute(
        budget_id=budget.id,
        name="New Name",
        balance=Decimal("250.50"),
        description="New description",
    )

    assert updated.id == budget.id
    assert updated.name == "New Name"
    assert updated.balance == Decimal("250.50")
    assert updated.description == "New description"
    assert updated.user_id == budget.user_id
    # Check that updated_at changed (created_at remains same)
    assert updated.updated_at > budget.updated_at


@pytest.mark.asyncio
async def test_update_budget_partial(update_budget: UpdateBudget, create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(
        name="Original", balance=Decimal("500.00"), user_id="user-123", description="Desc"
    )

    updated = await update_budget.execute(budget_id=budget.id, name="Changed Name")

    assert updated.name == "Changed Name"
    assert updated.balance == Decimal("500.00")  # unchanged
    assert updated.description == "Desc"  # unchanged


@pytest.mark.asyncio
async def test_update_budget_set_description_to_none(update_budget: UpdateBudget, create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(
        name="Budget", balance=Decimal(10), user_id="user-123", description="Some desc"
    )

    # Update description to None explicitly
    updated = await update_budget.execute(budget_id=budget.id, description=None)

    assert updated.description is None

    # Ensure that using UNSET leaves description unchanged
    updated2 = await update_budget.execute(budget_id=budget.id, name="Renamed")
    assert updated2.description is None  # still None, not reset to original


@pytest.mark.asyncio
async def test_update_budget_negative_balance(update_budget: UpdateBudget, create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(name="Budget", balance=Decimal(100), user_id="user-123")

    with pytest.raises(NegativeBalanceError, match="Balance cannot be negative: -1"):
        await update_budget.execute(budget_id=budget.id, balance=Decimal(-1))


@pytest.mark.asyncio
async def test_update_budget_empty_name(update_budget: UpdateBudget, create_budget: CreateBudget) -> None:
    budget = await create_budget.execute(name="Budget", balance=Decimal(100), user_id="user-123")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await update_budget.execute(budget_id=budget.id, name="")

    with pytest.raises(EmptyNameError, match="Name cannot be empty"):
        await update_budget.execute(budget_id=budget.id, name="   ")


@pytest.mark.asyncio
async def test_update_budget_not_found(update_budget: UpdateBudget) -> None:
    with pytest.raises(BudgetNotFoundError, match="Budget with id 'missing' not found"):
        await update_budget.execute(budget_id="missing", name="New Name")


@pytest.mark.asyncio
async def test_delete_budget_success(
    delete_budget: DeleteBudget, create_budget: CreateBudget, get_budget: GetBudget
) -> None:
    budget = await create_budget.execute(name="ToDelete", balance=Decimal(0), user_id="user-123")
    await delete_budget.execute(budget.id)

    with pytest.raises(BudgetNotFoundError):
        await get_budget.execute(budget.id)


@pytest.mark.asyncio
async def test_delete_budget_not_found(delete_budget: DeleteBudget) -> None:
    with pytest.raises(BudgetNotFoundError, match="Budget with id 'missing' not found"):
        await delete_budget.execute("missing")
