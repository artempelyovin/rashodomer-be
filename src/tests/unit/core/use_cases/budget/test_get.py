from unittest.mock import Mock

import pytest

from core.entities import Budget
from core.exceptions import BudgetAccessDeniedError, BudgetNotExistsError
from core.services import BudgetService
from core.use_cases.budget.get import GetBudgetUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = fake_budget
    use_case = GetBudgetUseCase(budget_service)

    budget = await use_case.get(user_id=fake_budget.user_id, budget_id=fake_budget.id)

    assert budget.name == fake_budget.name
    assert budget.description == fake_budget.description
    assert budget.amount == fake_budget.amount
    assert budget.user_id == fake_budget.user_id


async def test_budget_not_exists() -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = None
    use_case = GetBudgetUseCase(budget_service)

    with pytest.raises(BudgetNotExistsError):
        await use_case.get(user_id=str(fake.uuid4()), budget_id=str(fake.uuid4()))


async def test_budget_access_denied(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budget_service.get.return_value = fake_budget
    use_case = GetBudgetUseCase(budget_service)

    with pytest.raises(BudgetAccessDeniedError):
        await use_case.get(
            user_id=str(fake.uuid4()),  # another user
            budget_id=fake_budget.id,
        )
