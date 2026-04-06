from pathlib import Path

from app_ui.controllers.budget import BudgetCrudController
from domain.use_cases.budget import CreateBudget, DeleteBudget, ListBudgets, UpdateBudget
from infra.repos.file.budget import BudgetFileRepo


def build_budget_controller(base_dir: Path | None = None) -> BudgetCrudController:
    repo = BudgetFileRepo(base_dir=base_dir or Path("data/budgets"))
    return BudgetCrudController(
        create_budget_use_case=CreateBudget(repo),
        list_budgets_use_case=ListBudgets(repo),
        update_budget_use_case=UpdateBudget(repo),
        delete_budget_use_case=DeleteBudget(repo),
    )