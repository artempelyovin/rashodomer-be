import pytest


@pytest.mark.parametrize(
    "body",
    (
        {"name": "Cash", "description": None, "amount": 1000},
        {"name": "Cash", "description": "My cash", "amount": 150},
    ),
)
def test_create_budget__success(client, created_user, body: dict) -> None:
    response = client.post("/v1/budgets", json=body)

    assert response.status_code == 200, f"{response.text}"
    result = response.json()
    assert result["user_id"] == created_user.id
    for k, v in body.items():
        assert result[k] == v


def test_create_budget__amount_must_be_positive(client, created_user) -> None:
    response = client.post("/v1/budgets", json={"name": "cash", "amount": -100})

    assert response.status_code == 400, f"{response.text}"
    result = response.json()
    assert result["type"] == "AmountMustBePositive"
    assert result["detail"] == "Amount must be positive"


def test_create_budget__budget_already_exists(client, created_budget) -> None:
    response = client.post(
        "/v1/budgets", json={"name": created_budget.name, "amount": 10}
    )

    assert response.status_code == 400, f"{response.text}"
    result = response.json()
    assert result["type"] == "BudgetAlreadyExist"
    assert result["detail"] == f"Budget {created_budget.name} already exists"
