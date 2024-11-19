from unittest.mock import Mock

import pytest

from core.entities import Budget, Category, Transaction
from core.exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetNotExistsError,
    CategoryAccessDeniedError,
    CategoryNotExistsError,
)
from core.repos import BudgetRepository, CategoryRepository, TransactionRepository
from core.use_cases.transaction.create import CreateTransactionUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget, fake_category: Category, fake_transaction: Transaction) -> None:
    # user_id must match
    fake_budget.user_id = fake_transaction.user_id
    fake_category.user_id = fake_transaction.user_id

    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = fake_category
    transaction_service = Mock(spec=TransactionRepository)
    transaction_service.create.return_value = fake_transaction
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    transaction = await use_case.create(
        user_id=fake_transaction.user_id,
        amount=fake_transaction.amount,
        description=fake_transaction.description,
        transaction_type=fake_transaction.type,
        budget_id=fake_transaction.budget_id,
        category_id=fake_transaction.category_id,
        timestamp=fake_transaction.timestamp,
    )

    assert transaction == fake_transaction


async def test_amount_must_be_positive(fake_transaction: Transaction) -> None:
    budget_service = Mock(spec=BudgetRepository)
    category_service = Mock(spec=CategoryRepository)
    transaction_service = Mock(spec=TransactionRepository)
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    with pytest.raises(AmountMustBePositiveError):
        await use_case.create(
            user_id=fake_transaction.user_id,
            amount=fake.pyfloat(positive=False),  # negative
            description=fake_transaction.description,
            transaction_type=fake_transaction.type,
            budget_id=fake_transaction.budget_id,
            category_id=fake_transaction.category_id,
            timestamp=fake_transaction.timestamp,
        )


async def test_budget_not_exists(fake_transaction: Transaction) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = None
    category_service = Mock(spec=CategoryRepository)
    transaction_service = Mock(spec=TransactionRepository)
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    # Проверка исключения
    with pytest.raises(BudgetNotExistsError):
        await use_case.create(
            user_id=fake_transaction.user_id,
            amount=fake_transaction.amount,
            description=fake_transaction.description,
            transaction_type=fake_transaction.type,
            budget_id=fake_transaction.budget_id,
            category_id=fake_transaction.category_id,
            timestamp=fake_transaction.timestamp,
        )


async def test__budget_access_denied(fake_budget: Budget, fake_transaction: Transaction) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget  # another user_id
    category_service = Mock(spec=CategoryRepository)
    transaction_service = Mock(spec=TransactionRepository)
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    with pytest.raises(BudgetAccessDeniedError):
        await use_case.create(
            user_id=fake_transaction.user_id,
            amount=fake_transaction.amount,
            description=fake_transaction.description,
            transaction_type=fake_transaction.type,
            budget_id=fake_transaction.budget_id,
            category_id=fake_transaction.category_id,
            timestamp=fake_transaction.timestamp,
        )


async def test_category_not_exists(fake_budget: Budget, fake_transaction: Transaction) -> None:
    fake_budget.user_id = fake_transaction.user_id  # user_id must match for budget
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = None
    transaction_service = Mock(spec=TransactionRepository)
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    # Проверка исключения
    with pytest.raises(CategoryNotExistsError):
        await use_case.create(
            user_id=fake_transaction.user_id,
            amount=fake_transaction.amount,
            description=fake_transaction.description,
            transaction_type=fake_transaction.type,
            budget_id=fake_transaction.budget_id,
            category_id=fake_transaction.category_id,
            timestamp=fake_transaction.timestamp,
        )


async def test_category_access_denied(
    fake_budget: Budget, fake_category: Category, fake_transaction: Transaction
) -> None:
    fake_budget.user_id = fake_transaction.user_id  # user_id must match for budget
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget
    category_service = Mock(spec=CategoryRepository)
    category_service.get.return_value = fake_category  # another user_id
    transaction_service = Mock(spec=TransactionRepository)
    use_case = CreateTransactionUseCase(budget_service, category_service, transaction_service)

    with pytest.raises(CategoryAccessDeniedError):
        await use_case.create(
            user_id=fake_transaction.user_id,
            amount=fake_transaction.amount,
            description=fake_transaction.description,
            transaction_type=fake_transaction.type,
            budget_id=fake_transaction.budget_id,
            category_id=fake_transaction.category_id,
            timestamp=fake_transaction.timestamp,
        )
