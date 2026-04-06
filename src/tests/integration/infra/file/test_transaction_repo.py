from decimal import Decimal

import pytest

from domain.models.transaction import Transaction, TransactionType
from infra.repos.file.transaction import TransactionFileRepo


@pytest.mark.asyncio
async def test_create_and_get_by_id(transaction_repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1",
        budget_id="b_1",
        category_id="c_1",
        amount=Decimal("150.75"),
        type=TransactionType.EXPENSE,
        user_id="u_1",
        description="Lunch",
    )

    await transaction_repo.create(transaction)
    saved_tx = await transaction_repo.get_by_id("t_1")

    assert saved_tx == transaction


@pytest.mark.asyncio
async def test_get_by_user_id(transaction_repo: TransactionFileRepo) -> None:
    tx1 = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx2 = Transaction(
        id="t_2", budget_id="b_1", category_id="c_1", amount=Decimal(20), type=TransactionType.EXPENSE, user_id="u_2"
    )

    await transaction_repo.create(tx1)
    await transaction_repo.create(tx2)

    user1_txs = await transaction_repo.get_by_user_id("u_1")

    assert len(user1_txs) == 1
    assert user1_txs[0].id == "t_1"


@pytest.mark.asyncio
async def test_get_by_budget_id(transaction_repo: TransactionFileRepo) -> None:
    tx1 = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx2 = Transaction(
        id="t_2", budget_id="b_2", category_id="c_2", amount=Decimal(20), type=TransactionType.EXPENSE, user_id="u_1"
    )
    tx3 = Transaction(
        id="t_3", budget_id="b_1", category_id="c_2", amount=Decimal(30), type=TransactionType.INCOME, user_id="u_1"
    )

    await transaction_repo.create(tx1)
    await transaction_repo.create(tx2)
    await transaction_repo.create(tx3)

    budget1_txs = await transaction_repo.get_by_budget_id("b_1")

    assert len(budget1_txs) == 2
    assert tx1 in budget1_txs
    assert tx3 in budget1_txs


@pytest.mark.asyncio
async def test_update(transaction_repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    await transaction_repo.create(transaction)

    transaction.amount = Decimal(5000)
    transaction.description = "Updated description"
    await transaction_repo.update(transaction)

    updated_tx = await transaction_repo.get_by_id("t_1")
    assert updated_tx is not None
    assert updated_tx.amount == Decimal(5000)
    assert updated_tx.description == "Updated description"


@pytest.mark.asyncio
async def test_delete(transaction_repo: TransactionFileRepo) -> None:
    transaction = Transaction(
        id="t_1", budget_id="b_1", category_id="c_1", amount=Decimal(10), type=TransactionType.EXPENSE, user_id="u_1"
    )
    await transaction_repo.create(transaction)

    await transaction_repo.delete("t_1")

    assert await transaction_repo.get_by_id("t_1") is None
