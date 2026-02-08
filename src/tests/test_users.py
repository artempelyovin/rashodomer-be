def test_create_user__success(client) -> None:
    response = client.post(
        "/v1/users",
        json={
            "first_name": "Ivan",
            "last_name": "Petrov",
            "login": "vanya_petrov",
            "password": "******",
        },
    )

    assert response.status_code == 200, f"{response.text}"
    result = response.json()
    assert result["first_name"] == "Ivan"
    assert result["last_name"] == "Petrov"
    assert result["login"] == "vanya_petrov"
    assert result["last_login"] is not None


def test_create_user__login_already_exists(client, created_user) -> None:
    response = client.post(
        "/v1/users",
        json={
            "first_name": "Ivan",
            "last_name": "Petrov",
            "login": created_user.login,
            "password": "******",
        },
    )

    assert response.status_code == 400, f"{response.text}"
    result = response.json()
    assert result["type"] == "LoginAlreadyExist"
    assert result["detail"] == f"Login {created_user.login} already exists"


def test_get_user__success(client, created_user) -> None:
    response = client.get(f"v1/users/{created_user.id}")

    assert response.status_code == 200, f"{response.text}"
    result = response.json()
    assert result["id"] == created_user.id


def test_get_user__not_found(client) -> None:
    response = client.get(f"v1/users/not_existing_id")

    assert response.status_code == 404, f"{response.text}"
    result = response.json()
    assert result["type"] == "UserNotFound"
    assert result["detail"] == "User not_existing_id not found"
