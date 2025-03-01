from datetime import UTC, datetime, timedelta

from starlette import status
from starlette.testclient import TestClient

from base import ISO_TIMEZONE_FORMAT
from schemas.category import CategorySchema
from schemas.transaction import TransactionSchema
from schemas.user import UserSchema
from tests.integration.conftest import fake
from tests.integration.utils import register_and_authenticate


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

    def test_category_not_exists(self, client: TestClient, created_user: UserSchema) -> None:
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
            url=f"/v1/transactions",
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
            url=f"/v1/transactions",
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
