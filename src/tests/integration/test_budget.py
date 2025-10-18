from typing import Any

import pytest
from starlette import status
from starlette.testclient import TestClient

from models import ISO_TIMEZONE_FORMAT, BudgetSchema, UserSchema
from tests.integration.conftest import fake
from tests.integration.utils import create_budget, register_and_authenticate


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"name": "New Name", "description": "New description", "amount": 400}),
        ("DELETE", None),
    ],
)
def test_budget_not_exists(
    method: str,
    payload: dict[str, Any] | None,
    client: TestClient,
    created_user: UserSchema,  # noqa: ARG001
) -> None:
    non_existent_id = "12345"

    response = client.request(method=method, url=f"/v1/budgets/{non_existent_id}", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()["error"]
    assert error["type"] == "BudgetNotExistsError"
    assert error["detail"] == f"Budget with ID '{non_existent_id}' does not exist"


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"name": "New Name", "description": "New description", "amount": 400}),
        ("DELETE", None),
    ],
)
def test_budget_access_denied(
    method: str, payload: dict[str, Any] | None, client: TestClient, created_budget: BudgetSchema
) -> None:
    _, another_token = register_and_authenticate(
        client=client,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        login=fake.user_name(),
        password=fake.password(),
    )

    response = client.request(
        method=method,
        url=f"/v1/budgets/{created_budget.id}",
        json=payload,
        headers={"Authorization": another_token},  # <-- trying to get access by another user
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    error = response.json()["error"]
    assert error["type"] == "BudgetAccessDeniedError"
    assert error["detail"] == "Attempt to access another user's budget"


class TestBudgetCreate:
    def test_ok(self, client: TestClient, created_user: UserSchema) -> None:
        name = "Cash"
        description = "A budget for tracking all cash transactions and managing daily expenses"
        amount = 100
        response = client.post(
            "/v1/budgets",
            json={
                "name": "Cash",
                "description": "A budget for tracking all cash transactions and managing daily expenses",
                "amount": amount,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()["result"]
        assert result["id"]
        assert result["name"] == name
        assert result["description"] == description
        assert result["amount"] == amount
        assert result["user_id"] == created_user.id
        assert result["created_at"]
        assert result["updated_at"]

    def test_amount_must_be_positive(self, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002
        response = client.post(
            "/v1/budgets",
            json={
                "name": fake.word(),
                "description": fake.sentence(),
                "amount": fake.pyfloat(positive=False),  # <-- negative
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "AmountMustBePositiveError"
        assert error["detail"] == "Amount must be positive"

    def test_budget_already_exists(self, client: TestClient, created_budget: BudgetSchema) -> None:
        response = client.post(
            "/v1/budgets",
            json={
                "name": created_budget.name,  # <-- a second attempt to create budget with the same name
                "description": fake.sentence(),
                "amount": fake.pyfloat(positive=True),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "BudgetAlreadyExistsError"
        assert error["detail"] == f"A budget with the name '{created_budget.name}' already exists"


class TestBudgetGet:
    def test_ok(self, client: TestClient, created_budget: BudgetSchema, created_user: UserSchema) -> None:
        response = client.get(f"/v1/budgets/{created_budget.id}")

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result["id"] == created_budget.id
        assert result["name"] == created_budget.name
        assert result["description"] == created_budget.description
        assert result["amount"] == created_budget.amount
        assert result["user_id"] == created_user.id
        assert result["created_at"] == created_budget.created_at.strftime(ISO_TIMEZONE_FORMAT)
        assert result["updated_at"] == created_budget.updated_at.strftime(ISO_TIMEZONE_FORMAT)


class TestBudgetList:
    def test_success(self, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002
        expected_budgets = [
            create_budget(
                client=client, name=fake.word(), description=fake.sentence(), amount=fake.pyfloat(positive=True)
            )
            for _ in range(3)
        ]
        expected_budgets_by_id = {budget.id: budget for budget in expected_budgets}

        response = client.get("/v1/budgets")

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result["total"] == len(expected_budgets)
        budgets = result["items"]
        budgets_by_id = {budget["id"]: budget for budget in budgets}
        for expected_budget_id, expected_budget in expected_budgets_by_id.items():
            assert expected_budget_id in budgets_by_id
            assert expected_budget == BudgetSchema(**budgets_by_id[expected_budget_id])


class TestBudgetUpdate:
    def test_ok(self, client: TestClient, created_budget: BudgetSchema, created_user: UserSchema) -> None:
        updated_payload = {"name": "New Name", "description": "New description", "amount": 400}

        response = client.patch(f"/v1/budgets/{created_budget.id}", json=updated_payload)

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        # without changes
        assert result["id"] == created_budget.id
        assert result["user_id"] == created_user.id
        assert result["created_at"] == created_budget.created_at.strftime(ISO_TIMEZONE_FORMAT)
        # changed
        assert result["name"] == updated_payload["name"]
        assert result["description"] == updated_payload["description"]
        assert result["amount"] == updated_payload["amount"]
        assert result["updated_at"] != created_budget.updated_at.strftime(ISO_TIMEZONE_FORMAT)

    def test_amount_must_be_positive(self, client: TestClient, created_budget: BudgetSchema) -> None:
        response = client.patch(
            f"/v1/budgets/{created_budget.id}",
            json={
                "name": "New Name",
                "description": "New description",
                "amount": -200,  # <-- negative
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "AmountMustBePositiveError"
        assert error["detail"] == "Amount must be positive"


class TestBudgetDelete:
    def test_ok(self, client: TestClient, created_budget: BudgetSchema) -> None:
        response = client.delete(f"/v1/budgets/{created_budget.id}")

        assert response.status_code == status.HTTP_200_OK
        budget = BudgetSchema(**response.json()["result"])
        assert budget == created_budget


class TestBudgetFind:
    @pytest.mark.parametrize("search_in_name", [True, False])
    def test_ok(self, search_in_name: bool, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002, FBT001
        search_text = "cash"
        created_budget = create_budget(
            client=client,
            name=f"my {search_text}" if search_in_name else "some budget",
            description="some description" if search_in_name else f"description with {search_text}",
            amount=700,
        )

        response = client.get("/v1/budgets/find", params={"text": search_text, "case_sensitive": False})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result["total"] == 1
        budget = BudgetSchema(**result["items"][0])
        assert budget == created_budget
        if search_in_name:
            assert search_text in budget.name
        else:
            assert search_text in budget.description

    def test_empty_budget_text(self, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002
        response = client.get("/v1/budgets/find", params={"text": ""})  # empty text

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "EmptySearchTextError"
        assert error["detail"] == "Search text cannot be empty"
