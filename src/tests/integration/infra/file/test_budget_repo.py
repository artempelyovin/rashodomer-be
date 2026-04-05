from decimal import Decimal
from pathlib import Path

import pytest

from domain.models.budget import Budget
from infra.repos.file.budget import BudgetFileRepo


@pytest.fixture
def repo() -> BudgetFileRepo:
    return BudgetFileRepo(base_dir=Path("/tmp/budgets"))  # noqa: S108


@pytest.mark.asyncio
async def test_create_and_get_by_id(repo: BudgetFileRepo) -> None:
    budget = Budget(
        id="b_1",
        name="Main Budget",
        balance=Decimal("1000.50"),
        user_id="u_1",
    )

    await repo.create(budget)
    saved_budget = await repo.get_by_id("b_1")

    assert saved_budget == budget


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo: BudgetFileRepo) -> None:
    result = await repo.get_by_id("non_existent")
    assert result is None


@pytest.mark.asyncio
async def test_get_by_user_id(repo: BudgetFileRepo) -> None:
    budget1 = Budget(id="b_1", name="B1", balance=Decimal(0), user_id="u_1")
    budget2 = Budget(id="b_2", name="B2", balance=Decimal(0), user_id="u_1")
    budget3 = Budget(id="b_3", name="B3", balance=Decimal(0), user_id="u_2")

    await repo.create(budget1)
    await repo.create(budget2)
    await repo.create(budget3)

    user1_budgets = await repo.get_by_user_id("u_1")
    user2_budgets = await repo.get_by_user_id("u_2")

    assert len(user1_budgets) == 2
    assert budget1 in user1_budgets
    assert budget2 in user1_budgets
    assert len(user2_budgets) == 1
    assert budget3 in user2_budgets


@pytest.mark.asyncio
async def test_update(repo: BudgetFileRepo) -> None:
    budget = Budget(id="b_1", name="Old Name", balance=Decimal(0), user_id="u_1")
    await repo.create(budget)

    budget.name = "New Name"
    budget.balance = Decimal(500)
    await repo.update(budget)

    updated_budget = await repo.get_by_id("b_1")
    assert updated_budget is not None
    assert updated_budget.name == "New Name"
    assert updated_budget.balance == Decimal(500)


@pytest.mark.asyncio
async def test_delete(repo: BudgetFileRepo) -> None:
    budget = Budget(id="b_1", name="To Delete", balance=Decimal(0), user_id="u_1")
    await repo.create(budget)

    await repo.delete("b_1")
    deleted_budget = await repo.get_by_id("b_1")

    assert deleted_budget is None
