from decimal import Decimal
from pathlib import Path

import pytest

from domain.models.transaction import Transaction, TransactionType
from infra.repos.file.transaction import TransactionFileRepo


@pytest.fixture
def repo() -> TransactionFileRepo:
    return TransactionFileRepo(base_dir=Path("/tmp/transactions"))  # noqa: S108


@pytest.mark.asyncio
async def test_create_and_get_by_id(repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1",
        budget_id="b_1",
        category_id="c_1",
        amount=Decimal("150.75"),
        type=TransactionType.EXPENSE,
        user_id="u_1",
        description="Lunch",
    )

    await repo.create(transaction)
    saved_tx = await repo.get_by_id("t_1")

    assert saved_tx == transaction


@pytest.mark.asyncio
async def test_get_by_user_id(repo: TransactionFileRepo) -> None:
    tx1 = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx2 = Transaction(
        id="t_2", budget_id="b_1", category_id="c_1", amount=Decimal(20), type=TransactionType.EXPENSE, user_id="u_2"
    )

    await repo.create(tx1)
    await repo.create(tx2)

    user1_txs = await repo.get_by_user_id("u_1")

    assert len(user1_txs) == 1
    assert user1_txs[0].id == "t_1"


@pytest.mark.asyncio
async def test_get_by_budget_id(repo: TransactionFileRepo) -> None:
    tx1 = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx2 = Transaction(
        id="t_2", budget_id="b_2", category_id="c_2", amount=Decimal(20), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx3 = Transaction(
        id="t_3", budget_id="b_1", category_id="c_2", amount=Decimal(30), type=TransactionType.INCOME, user_id="u_1"
    )

    await repo.create(tx1)
    await repo.create(tx2)
    await repo.create(tx3)

    budget1_txs = await repo.get_by_budget_id("b_1")

    assert len(budget1_txs) == 2
    assert tx1 in budget1_txs
    assert tx3 in budget1_txs


@pytest.mark.asyncio
async def test_update(repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    await repo.create(transaction)

    transaction.amount = Decimal(5000)
    transaction.description = "Updated description"
    await repo.update(transaction)

    updated_tx = await repo.get_by_id("t_1")
    assert updated_tx is not None
    assert updated_tx.amount == Decimal(5000)
    assert updated_tx.description == "Updated description"


@pytest.mark.asyncio
async def test_delete(repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    await repo.create(transaction)

    await repo.delete("t_1")

    assert await repo.get_by_id("t_1") is None
