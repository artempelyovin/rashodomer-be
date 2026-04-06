from pathlib import Path

import pytest

from domain.use_cases.budget import CreateBudget, DeleteBudget, GetBudget, ListBudgets, UpdateBudget
from infra.repos.file.budget import BudgetFileRepo
from infra.repos.file.category import CategoryFileRepo
from infra.repos.file.transaction import TransactionFileRepo


@pytest.fixture
def budget_repo(tmp_path: Path) -> BudgetFileRepo:
    return BudgetFileRepo(base_dir=tmp_path / "budgets")


@pytest.fixture
def category_repo(tmp_path: Path) -> CategoryFileRepo:
    return CategoryFileRepo(base_dir=tmp_path / "categories")


@pytest.fixture
def transaction_repo(tmp_path: Path) -> TransactionFileRepo:
    return TransactionFileRepo(base_dir=tmp_path / "transactions")


@pytest.fixture
def create_budget(budget_repo: BudgetFileRepo) -> CreateBudget:
    return CreateBudget(budget_repo)


@pytest.fixture
def get_budget(budget_repo: BudgetFileRepo) -> GetBudget:
    return GetBudget(budget_repo)


@pytest.fixture
def list_budgets(budget_repo: BudgetFileRepo) -> ListBudgets:
    return ListBudgets(budget_repo)


@pytest.fixture
def update_budget(budget_repo: BudgetFileRepo) -> UpdateBudget:
    return UpdateBudget(budget_repo)


@pytest.fixture
def delete_budget(budget_repo: BudgetFileRepo) -> DeleteBudget:
    return DeleteBudget(budget_repo)
