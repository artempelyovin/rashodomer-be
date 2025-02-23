from starlette import status
from starlette.testclient import TestClient

from enums import CategoryType
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.user import TokenSchema, UserSchema


def register(client: TestClient, first_name: str, last_name: str, login: str, password: str) -> UserSchema:
    response = client.post(
        "/v1/register",
        json={"first_name": first_name, "last_name": last_name, "login": login, "password": password},
    )
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"Register error ({response.status_code} status code): {response.text}"
    return UserSchema(**response.json()["result"])


def authenticate(client: TestClient, login: str, password: str) -> str:
    response = client.post("/v1/login", json={"login": login, "password": password})
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"Authenticate error ({response.status_code} status code): {response.text}"
    return TokenSchema(**response.json()["result"]).token


def register_and_authenticate(
    client: TestClient, first_name: str, last_name: str, login: str, password: str
) -> tuple[UserSchema, str]:
    user = register(client, first_name, last_name, login, password)
    token = authenticate(client, login, password)
    return user, token


def create_budget(client: TestClient, name: str, description: str, amount: float) -> BudgetSchema:
    response = client.post("/v1/budgets", json={"name": name, "description": description, "amount": amount})
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"Create budget error ({response.status_code} status code): {response.text}"
    return BudgetSchema(**response.json()["result"])


def create_category(
    client: TestClient, name: str, description: str, category_type: CategoryType, emoji_icon: str | None
) -> CategorySchema:
    response = client.post(
        "/v1/categories",
        json={"name": name, "description": description, "type": category_type.name, "emoji_icon": emoji_icon},
    )
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"Create category error ({response.status_code} status code): {response.text}"
    return CategorySchema(**response.json()["result"])
