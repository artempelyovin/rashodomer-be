# ruff: noqa: ARG001, ARG002
from typing import Any

import pytest
from starlette import status
from starlette.testclient import TestClient

from base import ISO_TIMEZONE_FORMAT
from enums import CategoryType
from schemas.category import CategorySchema
from schemas.user import UserSchema
from tests.integration.conftest import fake
from tests.integration.utils import create_category, register_and_authenticate


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"name": "New Name", "description": "New description", "amount": 400}),
        ("DELETE", None),
    ],
)
def test_category_not_exists(
    method: str,
    payload: dict[str, Any] | None,
    client: TestClient,
    created_user: UserSchema,
) -> None:
    non_existent_id = "12345"

    response = client.request(method=method, url=f"/v1/categories/{non_existent_id}", json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error["type"] == "CategoryNotExistsError"
    assert error["detail"] == f"Category with ID '{non_existent_id}' does not exist"


@pytest.mark.parametrize(
    ("method", "payload"),
    [
        ("GET", None),
        ("PATCH", {"name": "New Name", "description": "New description", "amount": 400}),
        ("DELETE", None),
    ],
)
def test_category_access_denied(
    method: str, payload: dict[str, Any] | None, client: TestClient, created_category: CategorySchema
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
        url=f"/v1/categories/{created_category.id}",
        json=payload,
        headers={"Authorization": another_token},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    error = response.json()
    assert error["type"] == "CategoryAccessDeniedError"
    assert error["detail"] == "Attempt to access another user's category"


class TestCategoryCreate:
    @pytest.mark.parametrize("category_type", list(CategoryType))
    @pytest.mark.parametrize("emoji_icon", ["🤪", None])
    def test_ok(
        self, category_type: CategoryType, emoji_icon: str | None, client: TestClient, created_user: UserSchema
    ) -> None:
        payload = {
            "name": "new category",
            "description": "some desc",
            "type": category_type.name,
            "emoji_icon": emoji_icon,
        }
        response = client.post("/v1/categories", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        result = response.json()
        assert result["id"]
        assert result["name"] == payload["name"]
        assert result["description"] == payload["description"]
        assert result["type"] == payload["type"]
        assert result["emoji_icon"] == payload["emoji_icon"]
        assert result["is_archived"] is False
        assert result["user_id"] == created_user.id
        assert result["created_at"]
        assert result["updated_at"]

    def test_ok_with_same_name_but_different_category_type(
        self, client: TestClient, created_category: CategorySchema
    ) -> None:
        another_type = fake.random_element(set(CategoryType) - {created_category.type})

        response = client.post(
            "/v1/categories",
            json={
                "name": created_category.name,
                "description": "some desc",
                "type": another_type.name,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_category_name(self, client: TestClient, created_user: UserSchema) -> None:
        response = client.post(
            "/v1/categories",
            json={
                "name": "",
                "description": "some desc",
                "type": CategoryType.EXPENSE.name,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert error["type"] == "EmptyCategoryNameError"
        assert error["detail"] == "Category name cannot be empty"

    @pytest.mark.parametrize("bad_emoji_icon", ["🍿s", "not emodj", "s", ""])
    def test_not_emoji_icon(self, bad_emoji_icon: str, client: TestClient, created_user: UserSchema) -> None:
        response = client.post(
            "/v1/categories",
            json={
                "name": "new category",
                "description": "some desc",
                "type": CategoryType.EXPENSE.name,
                "emoji_icon": bad_emoji_icon,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert error["type"] == "NotEmojiIconError"
        assert error["detail"] == f"The provided icon in text format '{bad_emoji_icon}' is not a valid emoji"

    def test_category_already_exists(self, client: TestClient, created_category: CategorySchema) -> None:
        response = client.post(
            "/v1/categories",
            json={
                "name": created_category.name,
                "description": "some desc",
                "type": created_category.type.name,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert error["type"] == "CategoryAlreadyExistsError"
        assert (
            error["detail"]
            == f"A category with the name '{created_category.name}' and type '{created_category.type}' already exists"
        )


class TestCategoryGet:
    def test_ok(self, client: TestClient, created_category: CategorySchema) -> None:
        response = client.get(f"/v1/categories/{created_category.id}")

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == created_category.id
        assert result["name"] == created_category.name
        assert result["description"] == created_category.description
        assert result["type"] == created_category.type.name
        assert result["emoji_icon"] == created_category.emoji_icon
        assert result["is_archived"] is False
        assert result["user_id"] == created_category.user_id
        assert result["created_at"]
        assert result["updated_at"]


class TestCategoryList:
    @pytest.mark.parametrize("category_type", list(CategoryType))
    def test_ok(self, category_type: CategoryType, client: TestClient, created_user: UserSchema) -> None:
        expected_categories = [
            create_category(
                client=client,
                name=fake.word(),
                description=fake.sentence(),
                category_type=category_type,
                emoji_icon=fake.random_element([None, fake.emoji()]),
            )
            for _ in range(3)
        ]
        expected_categories_by_id = {category.id: category for category in expected_categories}

        response = client.get("/v1/categories", params={"category_type": category_type.name})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["total"] == len(expected_categories)
        categories = result["items"]
        categories_by_id = {category["id"]: category for category in categories}
        for expected_category_id, expected_category in expected_categories_by_id.items():
            assert expected_category_id in categories_by_id
            assert expected_category == CategorySchema(**categories_by_id[expected_category_id])


class TestCategoryUpdate:
    def test_ok(self, client: TestClient, created_category: CategorySchema, created_user: UserSchema) -> None:
        updated_payload = {
            "name": "New Name",
            "description": "New description",
            "type": fake.random_element(list(CategoryType)).name,
            "emoji_icon": fake.random_element([None, fake.emoji()]),
            "is_archived": fake.pybool(),
        }

        response = client.patch(f"/v1/categories/{created_category.id}", json=updated_payload)

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["id"] == created_category.id
        assert result["user_id"] == created_user.id
        assert result["created_at"] == created_category.created_at.strftime(ISO_TIMEZONE_FORMAT)
        assert result["name"] == updated_payload["name"]
        assert result["description"] == updated_payload["description"]
        assert result["type"] == updated_payload["type"]
        assert result["emoji_icon"] == updated_payload["emoji_icon"]
        assert result["is_archived"] == updated_payload["is_archived"]
        assert result["updated_at"] != created_category.updated_at.strftime(ISO_TIMEZONE_FORMAT)

    @pytest.mark.parametrize("bad_emoji_icon", ["🍿s", "not emoji", "s", ""])
    def test_not_emoji_icon(self, bad_emoji_icon: str, client: TestClient, created_category: CategorySchema) -> None:
        updated_payload = {
            "name": "New Name",
            "description": "New description",
            "type": fake.random_element(list(CategoryType)).name,
            "emoji_icon": bad_emoji_icon,
            "is_archived": fake.pybool(),
        }

        response = client.patch(f"/v1/categories/{created_category.id}", json=updated_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert error["type"] == "NotEmojiIconError"
        assert error["detail"] == f"The provided icon in text format '{bad_emoji_icon}' is not a valid emoji"


class TestCategoryDelete:
    def test_ok(self, client: TestClient, created_category: CategorySchema) -> None:
        response = client.delete(f"/v1/categories/{created_category.id}")

        assert response.status_code == status.HTTP_200_OK
        category = CategorySchema(**response.json())
        assert category == created_category


class TestCategoryFind:
    @pytest.mark.parametrize("search_in_name", [True, False])
    def test_ok(self, client: TestClient, created_user: UserSchema, *, search_in_name: bool) -> None:
        search_text = "car"
        created_category = create_category(
            client=client,
            name=f"my {search_text}" if search_in_name else "some category",
            description="some description" if search_in_name else f"description with {search_text}",
            category_type=fake.random_element(list(CategoryType)),
            emoji_icon=fake.random_element([None, fake.emoji()]),
        )

        response = client.get("/v1/categories/find", params={"text": search_text, "case_sensitive": False})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["total"] == 1
        category = CategorySchema(**result["items"][0])
        assert category == created_category
        if search_in_name:
            assert search_text in category.name
        else:
            assert search_text in category.description

    def test_empty_category_text(self, client: TestClient, created_user: UserSchema) -> None:
        response = client.get("/v1/categories/find", params={"text": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = response.json()
        assert error["type"] == "EmptySearchTextError"
        assert error["detail"] == "Search text cannot be empty"
