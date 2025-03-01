from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from starlette import status
from starlette.testclient import TestClient

from base import ISO_TIMEZONE_FORMAT
from enums import CategoryType
from schemas.category import CategorySchema
from schemas.transaction import TransactionSchema
from schemas.user import UserSchema
from tests.integration.conftest import fake
from tests.integration.utils import create_category, create_transaction, register_and_authenticate


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"amount": 1000, "description": "New description"}),
        ("DELETE", None),
    ],
)
def test_transaction_not_exists(
    method: str,
    payload: dict[str, Any] | None,
    client: TestClient,
    created_user: UserSchema,  # noqa: ARG001
) -> None:
    non_existent_id = "12345"

    response = client.request(method=method, url=f"/v1/transactions/{non_existent_id}", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()["error"]
    assert error["type"] == "TransactionNotExistsError"
    assert error["detail"] == f"Transaction with ID '{non_existent_id}' does not exist"


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"amount": 1000, "description": "New description"}),
        ("DELETE", None),
    ],
)
def test_transaction_access_denied(
    method: str, payload: dict[str, Any] | None, client: TestClient, created_transaction: TransactionSchema
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
        url=f"/v1/transactions/{created_transaction.id}",
        json=payload,
        headers={"Authorization": another_token},  # <-- trying to get access by another user
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    error = response.json()["error"]
    assert error["type"] == "TransactionAccessDeniedError"
    assert error["detail"] == "Attempt to access another user's transaction"


class TestTransactionCreate:
    def test_ok(self, client: TestClient, created_category: CategorySchema) -> None:
        payload = {
            "amount": 10,
            "description": "my first transaction",
            "category_id": created_category.id,
            "timestamp": "2020-12-12T11:00:12.000000Z",
        }
        response = client.post("/v1/transactions", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()["result"]
        assert result["id"]
        assert result["amount"] == payload["amount"]
        assert result["description"] == payload["description"]
        assert result["category_id"] == created_category.id
        assert result["user_id"] == created_category.user_id
        assert result["timestamp"] == payload["timestamp"]
        assert result["created_at"]
        assert result["updated_at"]

    def test_amount_must_be_positive(self, client: TestClient, created_category: CategorySchema) -> None:
        response = client.post(
            "/v1/transactions",
            json={
                "amount": -1,  # <-- negative
                "category_id": created_category.id,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "AmountMustBePositiveError"
        assert error["detail"] == "Amount must be positive"

    def test_category_not_exists(self, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002
        non_existent_id = "12345"

        response = client.post("/v1/transactions", json={"amount": 10, "category_id": non_existent_id})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()["error"]
        assert error["type"] == "CategoryNotExistsError"
        assert error["detail"] == f"Category with ID '{non_existent_id}' does not exist"

    def test_category_access_denied(self, client: TestClient, created_category: CategorySchema) -> None:
        _, another_token = register_and_authenticate(
            client=client,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            login=fake.user_name(),
            password=fake.password(),
        )

        response = client.post(
            url="/v1/transactions",
            json={"amount": 10, "category_id": created_category.id},
            headers={"Authorization": another_token},  # <-- trying to get access by another user
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        error = response.json()["error"]
        assert error["type"] == "CategoryAccessDeniedError"
        assert error["detail"] == "Attempt to access another user's category"

    def test_timestamp_in_future(self, client: TestClient, created_category: CategorySchema) -> None:
        future_timestamp = datetime.now(tz=UTC) + timedelta(days=1)

        response = client.post(
            url="/v1/transactions",
            json={
                "amount": 10,
                "category_id": created_category.id,
                "timestamp": future_timestamp.strftime(ISO_TIMEZONE_FORMAT),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "TimestampInFutureError"
        assert f"Timestamp '{future_timestamp}' cannot be in the future time. Current time:" in error["detail"]


class TestTransactionGet:
    def test_ok(self, client: TestClient, created_transaction: TransactionSchema) -> None:
        response = client.get(url=f"/v1/transactions/{created_transaction.id}")

        assert response.status_code == status.HTTP_200_OK
        transaction = TransactionSchema(**response.json()["result"])
        assert created_transaction == transaction


class TestTransactionList:
    def test_ok(self, client: TestClient, created_user: UserSchema, created_category: CategorySchema) -> None:  # noqa: ARG002
        expected_transactions = [
            create_transaction(
                client=client,
                amount=fake.pyfloat(positive=True),
                description=fake.sentence(),
                category_id=created_category.id,
                timestamp=fake.date_time_this_year(after_now=False),
            )
            for _ in range(3)
        ]
        expected_transactons_by_id = {transaction.id: transaction for transaction in expected_transactions}

        response = client.get("/v1/transactions")

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result["total"] == len(expected_transactions)
        transactions = result["items"]
        transactions_by_id = {transaction["id"]: transaction for transaction in transactions}
        for expected_transaction_id, expected_transaction in expected_transactons_by_id.items():
            assert expected_transaction_id in transactions_by_id
            assert expected_transaction == TransactionSchema(**transactions_by_id[expected_transaction_id])


class TestTransactionUpdate:
    def test_ok(self, client: TestClient, created_transaction: TransactionSchema, created_user: UserSchema) -> None:
        new_category = create_category(
            client=client,
            name="new_category",
            description="new category desc",
            category_type=CategoryType.EXPENSE,
            emoji_icon=fake.emoji(),
        )
        updated_payload = {
            "amount": 1000,
            "description": "New description",
            "category_id": new_category.id,
            "timestamp": datetime.now(tz=UTC).strftime(ISO_TIMEZONE_FORMAT),
        }

        response = client.patch(f"/v1/transactions/{created_transaction.id}", json=updated_payload)

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        # without changes
        assert result["id"] == created_transaction.id
        assert result["user_id"] == created_user.id
        assert result["created_at"] == created_transaction.created_at.strftime(ISO_TIMEZONE_FORMAT)
        # changed
        assert result["amount"] == updated_payload["amount"]
        assert result["description"] == updated_payload["description"]
        assert result["category_id"] == new_category.id
        assert result["timestamp"] == updated_payload["timestamp"]

    def test_amount_must_be_positive(self, client: TestClient, created_transaction: TransactionSchema) -> None:
        response = client.patch(
            f"/v1/transactions/{created_transaction.id}",
            json={"amount": -1},  # <-- negative
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "AmountMustBePositiveError"
        assert error["detail"] == "Amount must be positive"

    def test_category_not_found(self, client: TestClient, created_transaction: TransactionSchema) -> None:
        non_existent_id = "12345"

        response = client.patch(
            f"/v1/transactions/{created_transaction.id}",
            json={"category_id": non_existent_id},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()["error"]
        assert error["type"] == "CategoryNotExistsError"
        assert error["detail"] == f"Category with ID '{non_existent_id}' does not exist"

    def test_category_access_denied(self, client: TestClient, created_transaction: TransactionSchema) -> None:
        _, another_token = register_and_authenticate(
            client=client,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            login=fake.user_name(),
            password=fake.password(),
        )
        another_category = create_category(
            client=client,
            name="some category",
            description="some desc",
            category_type=CategoryType.EXPENSE,
            emoji_icon=None,
            headers={"Authorization": another_token},  # <-- a category created by another user
        )

        response = client.patch(
            f"/v1/transactions/{created_transaction.id}",
            json={"category_id": another_category.id},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        error = response.json()["error"]
        assert error["type"] == "CategoryAccessDeniedError"
        assert error["detail"] == "Attempt to access another user's category"


class TestTransactionDelete:
    def test_ok(self, client: TestClient, created_transaction: TransactionSchema) -> None:
        response = client.delete(f"/v1/transactions/{created_transaction.id}")

        assert response.status_code == status.HTTP_200_OK
        transaction = TransactionSchema(**response.json()["result"])
        assert transaction == created_transaction


class TestTransactionFind:
    def test_ok(self, client: TestClient, created_category: CategorySchema) -> None:
        search_text = "car"
        created_transaction = create_transaction(
            client=client,
            amount=10,
            description=f"description with {search_text}",
            category_id=created_category.id,
            timestamp=datetime.now(tz=UTC),
        )

        response = client.get("/v1/transactions/find", params={"text": search_text, "case_sensitive": False})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result["total"] == 1
        transaction = TransactionSchema(**result["items"][0])
        assert transaction == created_transaction
        assert search_text in transaction.description

    def test_empty_category_text(self, client: TestClient, created_user: UserSchema) -> None:  # noqa: ARG002
        response = client.get("/v1/transactions/find", params={"text": ""})  # empty text

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "EmptySearchTextError"
        assert error["detail"] == "Search text cannot be empty"
