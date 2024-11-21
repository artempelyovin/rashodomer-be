from unittest.mock import Mock

import pytest

from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAlreadyExistsError
from core.repos import BudgetRepository
from core.use_cases.budget.create import CreateBudgetUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.list_.return_value = (0, [])
    budget_service.create.return_value = fake_budget
    use_case = CreateBudgetUseCase(budget_service)

    budget = await use_case.create(
        name=fake_budget.name,
        description=fake_budget.description,
        amount=fake_budget.amount,
        user_id=fake_budget.user_id,
    )

    assert budget == fake_budget


async def test_amount_must_be_positive(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetRepository)
    use_case = CreateBudgetUseCase(budget_service)

    with pytest.raises(AmountMustBePositiveError):
        await use_case.create(
            name=fake_budget.name,
            description=fake_budget.description,
            amount=fake.pyfloat(positive=False),  # <-- negative
            user_id=fake_budget.user_id,
        )


async def test_budget_already_exist(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.list_.return_value = (1, [fake_budget])
    use_case = CreateBudgetUseCase(budget_service)

    with pytest.raises(BudgetAlreadyExistsError):
        await use_case.create(
            name=fake_budget.name,  # <-- name already exist
            description=fake_budget.description,
            amount=fake_budget.amount,
            user_id=fake_budget.user_id,
        )
