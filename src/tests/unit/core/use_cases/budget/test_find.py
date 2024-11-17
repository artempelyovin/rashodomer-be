from unittest.mock import Mock

import pytest

from core.entities import Budget
from core.exceptions import EmptySearchTextError
from core.services import BudgetService
from core.use_cases.budget.find import FindBudgetUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    budgets = [fake_budget]
    total = len(budgets)
    budget_service.find_by_text.return_value = (total, budgets)
    use_case = FindBudgetUseCase(budget_service)

    result_total, result_budgets = await use_case.find(
        user_id=str(fake.uuid4()), text="наличные", case_sensitive=fake.pybool(), limit=None, offset=0
    )

    assert result_total == total
    assert len(result_budgets) == len(budgets)
    for budget in budgets:
        assert budget in result_budgets


async def test_empty_budget_text() -> None:
    budget_service = Mock(spec=BudgetService)
    use_case = FindBudgetUseCase(budget_service)

    with pytest.raises(EmptySearchTextError):
        await use_case.find(
            user_id=str(fake.uuid4()), text="", case_sensitive=fake.pybool(), limit=fake.pyint(), offset=fake.pyint()
        )
