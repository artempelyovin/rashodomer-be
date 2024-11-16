from unittest.mock import Mock

import pytest

from core.entities import User
from core.exceptions import LoginAlreadyExistsError, PasswordMissingSpecialCharacterError, PasswordTooShortError
from core.services import PasswordService, UserService
from core.use_cases.auth.register import RegisterUserUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_user: User) -> None:
    user_service = Mock(spec=UserService)
    user_service.find_by_login.return_value = None  # No existing user
    user_service.create.return_value = fake_user
    password_service = Mock(spec=PasswordService)
    password_service.hash_password.return_value = "hashed_password"

    use_case = RegisterUserUseCase(user_service, password_service)

    registered_user = await use_case.register(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        login=fake.user_name(),
        password="ValidPassword1!",  # noqa: S106
    )

    assert registered_user == fake_user
    user_service.find_by_login.assert_called_once()
    user_service.create.assert_called_once()


async def test_login_already_exists(fake_user: User) -> None:
    user_service = Mock(spec=UserService)
    user_service.find_by_login.return_value = fake_user  # Existing user
    password_service = Mock(spec=PasswordService)

    use_case = RegisterUserUseCase(user_service, password_service)

    with pytest.raises(LoginAlreadyExistsError):
        await use_case.register(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            login=fake.user_name(),
            password="ValidPassword1!",  # noqa: S106
        )


async def test_password_too_short() -> None:
    user_service = Mock(spec=UserService)
    user_service.find_by_login.return_value = None  # No existing user
    password_service = Mock(spec=PasswordService)

    use_case = RegisterUserUseCase(user_service, password_service)

    with pytest.raises(PasswordTooShortError):
        await use_case.register(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            login=fake.user_name(),
            password="Short1",  # noqa: S106
        )


async def test_password_missing_special_character() -> None:
    user_service = Mock(spec=UserService)
    user_service.find_by_login.return_value = None  # No existing user
    password_service = Mock(spec=PasswordService)

    use_case = RegisterUserUseCase(user_service, password_service)

    with pytest.raises(PasswordMissingSpecialCharacterError):
        await use_case.register(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            login=fake.user_name(),
            password="NoSpecialChar123",  # noqa: S106
        )
