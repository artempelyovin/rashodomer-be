from unittest.mock import Mock

import pytest

from exceptions import (
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UnauthorizedError,
    UserNotExistsError,
)
from managers.auth import AuthManager
from repos.abc import TokenRepo, UserRepo
from schemas.user import CreateUserSchema, UserSchema
from tests.unit.conftest import fake


@pytest.fixture
def user_repo():
    return Mock(spec=UserRepo)


@pytest.fixture
def token_repo():
    return Mock(spec=TokenRepo)


class TestAuthManagerAuthenticate:
    async def test_success(self, user_repo, token_repo, fake_user: UserSchema) -> None:
        user_repo.get.return_value = fake_user
        token_repo.get_user_id_by_token.return_value = fake_user.id
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        authenticated_user = await manager.authenticate(token=str(fake.uuid4()))

        assert authenticated_user == fake_user

    async def test_no_token(self, user_repo, token_repo) -> None:
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UnauthorizedError):
            await manager.authenticate(token=None)

    async def test_invalid_token(self, user_repo, token_repo) -> None:
        token_repo.get_user_id_by_token.return_value = None
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UnauthorizedError):
            await manager.authenticate(token=str(fake.uuid4()))

    async def test_user_not_exists(self, user_repo, token_repo) -> None:
        token_repo.get_user_id_by_token.return_value = str(fake.uuid4())
        user_repo.get.return_value = None
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UserNotExistsError):
            await manager.authenticate(token=str(fake.uuid4()))


class TestAuthManagerLogin:
    async def test_success(self, user_repo, token_repo, fake_user: UserSchema) -> None:
        password = "very_strong_password"
        fake_user.password_hash = AuthManager.hash_password(password)  # override hash
        user_repo.find_by_login.return_value = fake_user
        new_token = fake.uuid4()
        token_repo.create_new_token.return_value = new_token
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        token = await manager.login(login=fake_user.login, password=password)

        assert token == new_token
        user_repo.update_last_login.assert_called_once()

    async def test_login_not_exists(self, user_repo, token_repo) -> None:
        user_repo.find_by_login.return_value = None
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(LoginNotExistsError):
            await manager.login(login=fake.user_name(), password=fake.password())

    async def test_incorrect_password(self, user_repo, token_repo, fake_user: UserSchema) -> None:
        user_repo.find_by_login.return_value = fake_user
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(IncorrectPasswordError):
            await manager.login(login=fake_user.login, password=fake.password())


class TestAuthManagerRegister:
    async def test_success(self, user_repo, token_repo, fake_user: UserSchema) -> None:
        user_repo.find_by_login.return_value = None  # No existing user
        user_repo.add.return_value = fake_user
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        registered_user = await manager.register(
            data=CreateUserSchema(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                login=fake.user_name(),
                password="ValidPassword1!",  # noqa: S106
            )
        )

        assert registered_user == fake_user
        user_repo.find_by_login.assert_called_once()
        user_repo.add.assert_called_once()

    async def test_login_already_exists(self, user_repo, token_repo, fake_user: UserSchema) -> None:
        user_repo.find_by_login.return_value = fake_user  # Existing user
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(LoginAlreadyExistsError):
            await manager.register(
                data=CreateUserSchema(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    login=fake.user_name(),
                    password="ValidPassword1!",  # noqa: S106
                )
            )

    async def test_password_too_short(self, user_repo, token_repo) -> None:
        user_repo.find_by_login.return_value = None  # No existing user
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(PasswordTooShortError):
            await manager.register(
                data=CreateUserSchema(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    login=fake.user_name(),
                    password="Short1",  # noqa: S106
                )
            )

    async def test_password_missing_special_character(self, user_repo, token_repo) -> None:
        user_repo.find_by_login.return_value = None  # No existing user
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(PasswordMissingSpecialCharacterError):
            await manager.register(
                data=CreateUserSchema(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    login=fake.user_name(),
                    password="NoSpecialChar123",  # noqa: S106
                )
            )
