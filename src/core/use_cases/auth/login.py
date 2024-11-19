from datetime import UTC, datetime

from core.exceptions import IncorrectPasswordError, LoginNotExistsError
from core.repos import UserRepository
from core.services import PasswordService, TokenService


class LoginUserUseCase:
    def __init__(
        self, user_service: UserRepository, password_service: PasswordService, token_service: TokenService
    ) -> None:
        self._user_repo = user_service
        self._password_service = password_service
        self._token_service = token_service

    async def login(self, login: str, password: str) -> str:
        user = await self._user_repo.find_by_login(login=login)
        if not user:
            raise LoginNotExistsError(login=login)
        password_hash = self._password_service.hash_password(password)
        if not self._password_service.check_password(password=password, password_hash=password_hash):
            raise IncorrectPasswordError
        await self._user_repo.update_last_login(user_id=user.id, last_login=datetime.now(tz=UTC))
        return await self._token_service.create_new_token(user_id=user.id)
