from unittest.mock import Mock

from core.entities import Budget
from core.services import BudgetService
from core.use_cases.budget.list import ListBudgetUseCase


async def success(fake_budget: Budget) -> None:
    budget_service = Mock(spec=BudgetService)
    expected_budgets = [fake_budget, fake_budget]
    expected_total = len(expected_budgets)
    budget_service.find.return_value = (expected_total, expected_budgets)
    use_case = ListBudgetUseCase(budget_service)

    total, budgets = await use_case.list(user_id=fake_budget.user_id, limit=None, offset=0)

    assert total == expected_total
    assert len(budgets) == len(expected_budgets)
    for budget, expected_budget in zip(budgets, budgets, strict=True):
        assert budget == expected_budget
