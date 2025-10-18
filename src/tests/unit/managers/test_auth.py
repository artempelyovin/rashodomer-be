from unittest.mock import Mock

import pytest

from exceptions import (
    UnauthorizedError,
    UserNotExistsError,
)
from managers.auth import AuthManager
from repos.abc import TokenRepo, UserRepo
from schemas.user import DetailedUserSchema
from tests.unit.conftest import fake


@pytest.fixture
def user_repo() -> Mock:
    return Mock(spec=UserRepo)


@pytest.fixture
def token_repo() -> Mock:
    return Mock(spec=TokenRepo)


class TestAuthManagerAuthenticate:
    async def test_success(self, user_repo: Mock, token_repo: Mock, fake_user: DetailedUserSchema) -> None:
        user_repo.get.return_value = fake_user
        token_repo.get_user_id_by_token.return_value = fake_user.id
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        authenticated_user = await manager.authenticate(token=str(fake.uuid4()))

        assert authenticated_user == fake_user

    async def test_no_token(self, user_repo: Mock, token_repo: Mock) -> None:
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UnauthorizedError):
            await manager.authenticate(token=None)

    async def test_invalid_token(self, user_repo: Mock, token_repo: Mock) -> None:
        token_repo.get_user_id_by_token.return_value = None
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UnauthorizedError):
            await manager.authenticate(token=str(fake.uuid4()))

    async def test_user_not_exists(self, user_repo: Mock, token_repo: Mock) -> None:
        token_repo.get_user_id_by_token.return_value = str(fake.uuid4())
        user_repo.get.return_value = None
        manager = AuthManager(user_repo=user_repo, token_repo=token_repo)

        with pytest.raises(UserNotExistsError):
            await manager.authenticate(token=str(fake.uuid4()))
