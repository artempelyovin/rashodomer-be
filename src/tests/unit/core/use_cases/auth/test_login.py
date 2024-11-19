from unittest.mock import Mock

import pytest

from core.entities import User
from core.exceptions import IncorrectPasswordError, LoginNotExistsError
from core.services import PasswordService, TokenService
from core.repos import UserRepository
from core.use_cases.auth.login import LoginUserUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_user: User) -> None:
    user_service = Mock(spec=UserRepository)
    user_service.find_by_login.return_value = fake_user
    password_service = Mock(spec=PasswordService)
    password_service.hash_password.return_value = "hashed_password"
    password_service.check_password.return_value = True
    new_token = fake.uuid4()
    token_service = Mock(spec=TokenService)
    token_service.create_new_token.return_value = new_token

    use_case = LoginUserUseCase(user_service, password_service, token_service)

    token = await use_case.login(login=fake_user.login, password=fake.password())

    assert token == new_token
    user_service.update_last_login.assert_called_once()


async def test_login_not_exists() -> None:
    user_service = Mock(spec=UserRepository)
    user_service.find_by_login.return_value = None
    password_service = Mock(spec=PasswordService)
    token_service = Mock(spec=TokenService)

    use_case = LoginUserUseCase(user_service, password_service, token_service)

    with pytest.raises(LoginNotExistsError):
        await use_case.login(login=fake.user_name(), password=fake.password())


async def test_incorrect_password(fake_user: User) -> None:
    user_service = Mock(spec=UserRepository)
    user_service.find_by_login.return_value = fake_user
    password_service = Mock(spec=PasswordService)
    password_service.hash_password.return_value = "hashed_password"
    password_service.check_password.return_value = False
    token_service = Mock(spec=TokenService)

    use_case = LoginUserUseCase(user_service, password_service, token_service)

    with pytest.raises(IncorrectPasswordError):
        await use_case.login(login=fake_user.login, password=fake.password())
