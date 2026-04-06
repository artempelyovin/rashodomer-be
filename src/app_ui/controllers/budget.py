from dataclasses import dataclass
from decimal import Decimal

from app_ui.constants import DEFAULT_USER_ID
from domain.models.budget import Budget
from domain.use_cases.budget import CreateBudget, DeleteBudget, ListBudgets, UpdateBudget


@dataclass(slots=True)
class BudgetCrudController:
    create_budget_use_case: CreateBudget
    list_budgets_use_case: ListBudgets
    update_budget_use_case: UpdateBudget
    delete_budget_use_case: DeleteBudget
    user_id: str = DEFAULT_USER_ID

    async def list_budgets(self) -> list[Budget]:
        budgets = await self.list_budgets_use_case.execute(self.user_id)
        return sorted(budgets, key=lambda budget: budget.created_at, reverse=True)

    async def create_budget(self, name: str, balance: Decimal, description: str | None) -> Budget:
        return await self.create_budget_use_case.execute(
            name=name,
            balance=balance,
            user_id=self.user_id,
            description=self._normalize_description(description),
        )

    async def update_budget(self, budget_id: str, name: str, balance: Decimal, description: str | None) -> Budget:
        return await self.update_budget_use_case.execute(
            budget_id=budget_id,
            name=name,
            balance=balance,
            description=self._normalize_description(description),
        )

    async def delete_budget(self, budget_id: str) -> None:
        await self.delete_budget_use_case.execute(budget_id)

    @staticmethod
    def _normalize_description(description: str | None) -> str | None:
        if description is None:
            return None
        stripped = description.strip()
        return stripped or None