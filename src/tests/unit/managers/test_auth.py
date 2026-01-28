from unittest.mock import Mock

import pytest

from exceptions import (
    UnauthorizedError,
    UserNotExistsError,
)
from managers.auth import AuthManager
from schemas.user import DetailedUserSchema
from tests.unit.conftest import fake


class TestAuthManagerAuthenticate:
    async def test_success(self, user_repo: Mock, token_repo: Mock, fake_user: DetailedUserSchema) -> None:
        user_repo.get.return_value = fake_user
        token_repo.get_user_id_by_token.return_value = fake_user.id

        authenticated_user = await AuthManager.authenticate(token=str(fake.uuid4()))

        assert authenticated_user == fake_user

    async def test_no_token(self) -> None:

        with pytest.raises(UnauthorizedError):
            await AuthManager.authenticate(token=None)

    async def test_invalid_token(self) -> None:
        token_repo.get_user_id_by_token.return_value = None

        with pytest.raises(UnauthorizedError):
            await AuthManager.authenticate(token=str(fake.uuid4()))

    async def test_user_not_exists(self) -> None:
        token_repo.get_user_id_by_token.return_value = str(fake.uuid4())
        user_repo.get.return_value = None

        with pytest.raises(UserNotExistsError):
            await AuthManager.authenticate(token=str(fake.uuid4()))
