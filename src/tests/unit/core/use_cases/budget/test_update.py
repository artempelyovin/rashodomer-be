from unittest.mock import Mock

import pytest

from core.entities import Budget
from core.exceptions import AmountMustBePositiveError, BudgetAccessDeniedError, BudgetNotExistsError
from core.services import BudgetService
from core.use_cases.budget.update import UpdateBudgetUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    expected_budget = Budget(
        id=fake_budget.id,
        user_id=fake_budget.user_id,
        # updated params
        name=fake.word(),
        description=fake.sentence(),
        amount=fake.pyfloat(positive=True),
    )

    budget_service.get.return_value = fake_budget
    budget_service.update_budget.return_value = expected_budget
    use_case = UpdateBudgetUseCase(budget_service)

    updated_budget = await use_case.update(
        user_id=fake_budget.user_id,
        budget_id=fake_budget.id,
        name=expected_budget.name,
        description=expected_budget.description,
        amount=expected_budget.amount,
    )

    # unchanged
    assert updated_budget.id == fake_budget.id
    assert updated_budget.user_id == fake_budget.user_id
    # changed
    assert updated_budget.name == expected_budget.name
    assert updated_budget.description == expected_budget.description
    assert updated_budget.amount == expected_budget.amount


async def test_budget_not_exists(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = None
    use_case = UpdateBudgetUseCase(budget_service)

    with pytest.raises(BudgetNotExistsError):
        await use_case.update(
            user_id=fake_budget.user_id,
            budget_id=fake_budget.id,
            name=fake.word(),
            description=fake.sentence(),
            amount=fake.pyfloat(positive=True),
        )


async def test_budget_access_denied(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = fake_budget
    use_case = UpdateBudgetUseCase(budget_service)

    with pytest.raises(BudgetAccessDeniedError):
        await use_case.update(
            user_id=str(fake.uuid4()),  # another user
            budget_id=fake_budget.id,
            name=fake.word(),
            description=fake.sentence(),
            amount=fake.pyfloat(positive=True),
        )


async def test_amount_must_be_positive(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = fake_budget
    use_case = UpdateBudgetUseCase(budget_service)

    with pytest.raises(AmountMustBePositiveError):
        await use_case.update(
            user_id=fake_budget.user_id,
            budget_id=fake_budget.id,
            name=fake.word(),
            description=fake.sentence(),
            amount=fake.pyfloat(positive=False),  # negative
        )
