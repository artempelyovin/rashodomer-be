from starlette.testclient import TestClient

from schemas import UserSchema, BudgetSchema


def create_user(
    client: TestClient, first_name: str, last_name: str, login: str, password: str
) -> UserSchema:
    response = client.post(
        "/v1/users",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "login": login,
            "password": password,
        },
    )

    assert response.status_code == 200, f"Can't create user: {response.text}"
    return UserSchema.model_validate(response.json())


def create_budget(
    client: TestClient, name: str, description: str | None, amount: float
) -> BudgetSchema:
    response = client.post(
        "/v1/budgets",
        json={"name": name, "description": description, "amount": amount},
    )

    assert response.status_code == 200, f"Can't create budget: {response.text}"
    return BudgetSchema.model_validate(response.json())
