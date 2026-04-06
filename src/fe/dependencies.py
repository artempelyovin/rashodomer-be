from pathlib import Path

from domain.use_cases.budget import CreateBudget, DeleteBudget, GetBudget, ListBudgets, UpdateBudget
from infra.repos.file.budget import BudgetFileRepo

HARDCODED_USER_ID = "default-user-123"

budget_repo = BudgetFileRepo(base_dir=Path("data/budgets"))

create_budget_uc = CreateBudget(budget_repo)
get_budget_uc = GetBudget(budget_repo)
list_budgets_uc = ListBudgets(budget_repo)
update_budget_uc = UpdateBudget(budget_repo)
delete_budget_uc = DeleteBudget(budget_repo)
