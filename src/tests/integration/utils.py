from datetime import datetime

from starlette import status
from starlette.testclient import TestClient

from enums import CategoryType
from models import ISO_TIMEZONE_FORMAT, Budget, Category, Token, Transaction, User


def register(client: TestClient, first_name: str, last_name: str, login: str, password: str) -> User:
    response = client.post(
        "/v1/register",
        json={"first_name": first_name, "last_name": last_name, "login": login, "password": password},
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Register error ({response.status_code} status code): {response.text}"
    )
    return User(**response.json()["result"])


def authenticate(client: TestClient, login: str, password: str) -> str:
    response = client.post("/v1/login", json={"login": login, "password": password})
    assert response.status_code == status.HTTP_200_OK, (
        f"Authenticate error ({response.status_code} status code): {response.text}"
    )
    return Token(**response.json()["result"]).token


def register_and_authenticate(
    client: TestClient, first_name: str, last_name: str, login: str, password: str
) -> tuple[User, str]:
    user = register(client, first_name, last_name, login, password)
    token = authenticate(client, login, password)
    return user, token


def create_budget(
    client: TestClient, name: str, description: str, amount: float, headers: dict[str, str] | None = None
) -> Budget:
    response = client.post(
        "/v1/budgets", json={"name": name, "description": description, "amount": amount}, headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Create budget error ({response.status_code} status code): {response.text}"
    )
    return Budget(**response.json()["result"])


def create_category(
    client: TestClient,
    name: str,
    description: str,
    category_type: CategoryType,
    emoji_icon: str | None,
    headers: dict[str, str] | None = None,
) -> Category:
    response = client.post(
        "/v1/categories",
        json={"name": name, "description": description, "type": category_type.name, "emoji_icon": emoji_icon},
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Create category error ({response.status_code} status code): {response.text}"
    )
    return Category(**response.json()["result"])


def create_transaction(
    client: TestClient,
    amount: float,
    description: str,
    category_id: str,
    timestamp: datetime,
    headers: dict[str, str] | None = None,
) -> Transaction:
    response = client.post(
        "/v1/transactions",
        json={
            "amount": amount,
            "description": description,
            "category_id": category_id,
            "timestamp": timestamp.strftime(ISO_TIMEZONE_FORMAT),
        },
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Create transaction error ({response.status_code} status code): {response.text}"
    )
    return Transaction(**response.json()["result"])
