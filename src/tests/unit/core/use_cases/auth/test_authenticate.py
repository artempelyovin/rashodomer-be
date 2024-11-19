from unittest.mock import Mock

import pytest

from core.entities import User
from core.exceptions import UnauthorizedError, UserNotExistsError
from core.services import TokenService
from core.repos import UserRepository
from core.use_cases.auth.authenticate import AuthenticationUseCase
from tests.unit.core.conftest import fake


async def test_success(fake_user: User) -> None:
    token_service = Mock(spec=TokenService)
    token_service.get_user_id_by_token.return_value = fake_user.id
    user_service = Mock(spec=UserRepository)
    user_service.get.return_value = fake_user
    use_case = AuthenticationUseCase(token_service, user_service)

    authenticated_user = await use_case.authenticate(token=str(fake.uuid4()))

    assert authenticated_user == fake_user


async def test_no_token() -> None:
    token_service = Mock(spec=TokenService)
    user_service = Mock(spec=UserRepository)

    use_case = AuthenticationUseCase(token_service, user_service)

    with pytest.raises(UnauthorizedError):
        await use_case.authenticate(token=None)


async def test_invalid_token() -> None:
    token_service = Mock(spec=TokenService)
    token_service.get_user_id_by_token.return_value = None
    user_service = Mock(spec=UserRepository)

    use_case = AuthenticationUseCase(token_service, user_service)

    with pytest.raises(UnauthorizedError):
        await use_case.authenticate(token=str(fake.uuid4()))


async def test_user_not_exists() -> None:
    token_service = Mock(spec=TokenService)
    token_service.get_user_id_by_token.return_value = str(fake.uuid4())
    user_service = Mock(spec=UserRepository)
    user_service.get.return_value = None

    use_case = AuthenticationUseCase(token_service, user_service)

    with pytest.raises(UserNotExistsError):
        await use_case.authenticate(token=str(fake.uuid4()))
