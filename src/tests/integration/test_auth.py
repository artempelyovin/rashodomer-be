from starlette import status
from starlette.testclient import TestClient

from models import User
from tests.integration.utils import register


class TestRegister:
    def test_ok(self, client: TestClient) -> None:
        first_name = "ivanov"
        last_name = "ivanov"
        login = "ivan_ivanov"
        password = "qwerty123456!"  # noqa: S105

        response = client.post(
            "/v1/register",
            json={"first_name": first_name, "last_name": last_name, "login": login, "password": password},
        )

        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["result"]["id"]
        assert result["result"]["first_name"] == first_name
        assert result["result"]["last_name"] == last_name
        assert result["result"]["login"] == login
        assert result["result"]["created_at"]
        assert result["result"]["last_login"]

    def test_login_already_exists(self, client: TestClient, created_user: User) -> None:
        response = client.post(
            "/v1/register",
            json={
                "first_name": "new first name",
                "last_name": "new last name",
                "login": created_user.login,  # <-- existing login
                "password": "new password",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "LoginAlreadyExistsError"
        assert error["detail"] == f"Login '{created_user.login}' already exists"

    def test_password_too_short(self, client: TestClient) -> None:
        response = client.post(
            "/v1/register",
            json={
                "first_name": "new fist name",
                "last_name": "new last name",
                "login": "new login",
                "password": "short",  # <-- really short :D
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "PasswordTooShortError"
        assert error["detail"] == "Password is too short. It must be at least 8 characters long"

    def test_password_missing_special_character(self, client: TestClient) -> None:
        response = client.post(
            "/v1/register",
            json={
                "first_name": "new fist name",
                "last_name": "new last name",
                "login": "new login",
                "password": "withou special characters",  # <-- without !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "PasswordMissingSpecialCharacterError"
        assert error["detail"] == "Password is missing special character"


class TestLogin:
    def test_ok(self, client: TestClient) -> None:
        login = "mike_j"
        password = "Passw0rd!2024"  # noqa: S105
        register(client=client, first_name="johnson", last_name="johnson", login=login, password=password)

        response = client.post("/v1/login", json={"login": login, "password": password})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["result"]["token"]

    def test_login_not_exists(self, client: TestClient) -> None:
        unknown_login = "unknown_login"
        response = client.post("/v1/login", json={"login": unknown_login, "password": "unknown_password"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        error = response.json()["error"]
        assert error["type"] == "LoginNotExistsError"
        assert error["detail"] == f"Login '{unknown_login}' does not exist"

    def test_incorrect_password(self, client: TestClient, created_user: User) -> None:
        incorrect_password = "incorrect_password"  # noqa: S105

        response = client.post("/v1/login", json={"login": created_user.login, "password": incorrect_password})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()["error"]
        assert error["type"] == "IncorrectPasswordError"
        assert error["detail"] == "Incorrect password"
