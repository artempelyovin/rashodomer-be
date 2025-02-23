# ruff: noqa: PLR2004
import pytest
from starlette.testclient import TestClient

from app import fast_api

client = TestClient(fast_api)


class TestRegister:
    @pytest.mark.parametrize(
        ("first_name", "last_name", "login", "password"),
        [
            ("ivan", "ivanov", "ivan_ivanov", "qwerty123456!"),
            ("anna", "petrova", "anna_petrov", "securePass!2023"),
            ("sergey", "sidorov", "sergey_s", "Pa$w0rd2023"),
            ("elena", "nikolaeva", "elena_nikol", "Elena@2023"),
        ],
    )
    def test_ok(self, first_name: str, last_name: str, login: str, password: str) -> None:
        response = client.post(
            "/v1/register",
            json={"first_name": first_name, "last_name": last_name, "login": login, "password": password},
        )
        assert response.status_code == 201
        result = response.json()
        assert result["result"]["id"]
        assert result["result"]["first_name"] == first_name
        assert result["result"]["last_name"] == last_name
        assert result["result"]["login"] == login
        assert result["result"]["created_at"]
        assert result["result"]["last_login"]


class TestLogin:
    @pytest.mark.parametrize(
        ("first_name", "last_name", "login", "password"),
        [
            ("michael", "johnson", "mike_j", "Passw0rd!2024"),
            ("sarah", "williams", "sarah_w", "SecurePass#2024"),
            ("david", "brown", "dave_b", "MyP@ss2024"),
            ("emma", "davis", "emma_d", "Emma@Secure2024"),
        ],
    )
    def test_ok(self, first_name: str, last_name: str, login: str, password: str) -> None:
        response = client.post(
            "/v1/register",
            json={"first_name": first_name, "last_name": last_name, "login": login, "password": password},
        )
        assert response.status_code == 201

        response = client.post("/v1/login", json={"login": login, "password": password})
        assert response.status_code == 200
        result = response.json()
        assert result["result"]["token"]
