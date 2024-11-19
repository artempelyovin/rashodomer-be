from unittest.mock import Mock

import pytest

from core.entities import Budget
from core.exceptions import BudgetAccessDeniedError, BudgetNotExistsError
from core.repos import BudgetRepository
from core.use_cases.budget.delete import DeleteBudgetUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget
    budget_service.delete.return_value = fake_budget
    use_case = DeleteBudgetUseCase(budget_service)

    deleted_budget = await use_case.delete(user_id=fake_budget.user_id, budget_id=fake_budget.id)

    assert deleted_budget.user_id == fake_budget.user_id
    assert deleted_budget.name == fake_budget.name
    assert deleted_budget.description == fake_budget.description


async def test_budget_not_exists() -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = None
    use_case = DeleteBudgetUseCase(budget_service)

    with pytest.raises(BudgetNotExistsError):
        await use_case.delete(user_id=str(fake.uuid4()), budget_id=str(fake.uuid4()))


async def test_budget_access_denied(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetRepository)
    budget_service.get.return_value = fake_budget
    use_case = DeleteBudgetUseCase(budget_service)

    with pytest.raises(BudgetAccessDeniedError):
        await use_case.delete(
            user_id=str(fake.uuid4()),  # another user
            budget_id=fake_budget.id,
        )
