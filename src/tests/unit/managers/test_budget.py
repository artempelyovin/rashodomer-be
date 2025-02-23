from unittest.mock import Mock

import pytest

from exceptions import (
    AmountMustBePositiveError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    EmptySearchTextError,
)
from managers.budget import BudgetManager
from repos.abc import BudgetRepo
from schemas.budget import BudgetSchema, CreateBudgetSchema
from tests.unit.conftest import fake
from utils import UNSET


@pytest.fixture
def budget_repo():
    return Mock(spec=BudgetRepo)


class TestBudgetManagerCreate:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.find_by_name.return_value = (0, [])
        budget_repo.add.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        budget = await manager.create(
            user_id=fake_budget.user_id,
            data=CreateBudgetSchema(
                name=fake_budget.name,
                description=fake_budget.description,
                amount=fake_budget.amount,
            ),
        )

        assert budget.name == fake_budget.name
        assert budget.description == fake_budget.description
        assert budget.amount == fake_budget.amount
        assert budget.user_id == fake_budget.user_id

    async def test_amount_must_be_positive(self, budget_repo, fake_budget: BudgetSchema) -> None:
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(AmountMustBePositiveError):
            await manager.create(
                user_id=fake_budget.user_id,
                data=CreateBudgetSchema(
                    name=fake_budget.name,
                    description=fake_budget.description,
                    amount=fake.pyfloat(positive=False),  # <-- negative
                ),
            )

    async def test_budget_already_exist(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.find_by_name.return_value = (1, [fake_budget])
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetAlreadyExistsError):
            await manager.create(
                user_id=fake_budget.user_id,
                data=CreateBudgetSchema(
                    name=fake_budget.name,  # <-- name already exist
                    description=fake_budget.description,
                    amount=fake_budget.amount,
                ),
            )


class TestBudgetManagerGet:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        budget = await manager.get(user_id=fake_budget.user_id, budget_id=fake_budget.id)

        assert budget.name == fake_budget.name
        assert budget.description == fake_budget.description
        assert budget.amount == fake_budget.amount
        assert budget.user_id == fake_budget.user_id

    async def test_budget_not_exists(self, budget_repo) -> None:
        budget_repo.get.return_value = None
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetNotExistsError):
            await manager.get(user_id=str(fake.uuid4()), budget_id=str(fake.uuid4()))

    async def test_budget_access_denied(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetAccessDeniedError):
            await manager.get(
                user_id=str(fake.uuid4()),  # another user
                budget_id=fake_budget.id,
            )


class TestBudgetManagerList:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        expected_budgets = [fake_budget, fake_budget]
        expected_total = len(expected_budgets)
        budget_repo.list_.return_value = (expected_total, expected_budgets)
        manager = BudgetManager(budget_repo=budget_repo)

        total, budgets = await manager.list_(user_id=fake_budget.user_id, limit=None, offset=0)

        assert total == expected_total
        assert len(budgets) == len(expected_budgets)
        for budget, expected_budget in zip(budgets, budgets, strict=True):
            assert budget == expected_budget


class TestBudgetManagerUpdate:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        expected_budget = BudgetSchema(
            id=fake_budget.id,
            user_id=fake_budget.user_id,
            # updated params
            name=fake.word(),
            description=fake.sentence(),
            amount=fake.pyfloat(positive=True),
        )

        budget_repo.get.return_value = fake_budget
        budget_repo.update_budget.return_value = expected_budget
        manager = BudgetManager(budget_repo=budget_repo)

        updated_budget = await manager.update(
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

    async def test_budget_not_exists(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = None
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetNotExistsError):
            await manager.update(
                user_id=fake_budget.user_id,
                budget_id=fake_budget.id,
                name=UNSET,
                description=UNSET,
                amount=UNSET,
            )

    async def test_budget_access_denied(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetAccessDeniedError):
            await manager.update(
                user_id=str(fake.uuid4()),  # another user
                budget_id=fake_budget.id,
                name=UNSET,
                description=UNSET,
                amount=UNSET,
            )

    async def test_amount_must_be_positive(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(AmountMustBePositiveError):
            await manager.update(
                user_id=fake_budget.user_id,
                budget_id=fake_budget.id,
                name=fake.word(),
                description=fake.sentence(),
                amount=fake.pyfloat(positive=False),  # negative
            )


class TestBudgetManagerDelete:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        budget_repo.delete.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        deleted_budget = await manager.delete(user_id=fake_budget.user_id, budget_id=fake_budget.id)

        assert deleted_budget.user_id == fake_budget.user_id
        assert deleted_budget.name == fake_budget.name
        assert deleted_budget.description == fake_budget.description

    async def test_budget_not_exists(self, budget_repo) -> None:
        budget_repo.get.return_value = None
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetNotExistsError):
            await manager.delete(user_id=str(fake.uuid4()), budget_id=str(fake.uuid4()))

    async def test_budget_access_denied(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budget_repo.get.return_value = fake_budget
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(BudgetAccessDeniedError):
            await manager.delete(
                user_id=str(fake.uuid4()),  # another user
                budget_id=fake_budget.id,
            )


class TestBudgetManagerFind:
    async def test_success(self, budget_repo, fake_budget: BudgetSchema) -> None:
        budgets = [fake_budget]
        total = len(budgets)
        budget_repo.find_by_text.return_value = (total, budgets)
        manager = BudgetManager(budget_repo=budget_repo)

        result_total, result_budgets = await manager.find(
            user_id=str(fake.uuid4()), text="наличные", case_sensitive=fake.pybool(), limit=None, offset=0
        )

        assert result_total == total
        assert len(result_budgets) == len(budgets)
        for budget in budgets:
            assert budget in result_budgets

    async def test_empty_budget_text(self, budget_repo) -> None:
        manager = BudgetManager(budget_repo=budget_repo)

        with pytest.raises(EmptySearchTextError):
            await manager.find(
                user_id=str(fake.uuid4()),
                text="",
                case_sensitive=fake.pybool(),
                limit=fake.pyint(),
                offset=fake.pyint(),
            )
