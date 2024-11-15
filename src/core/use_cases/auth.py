from core.entities import User
from core.exceptions import UnauthorizedError, UserNotExistsError
from core.services import TokenService, UserService


class AuthenticationUseCase:
    def __init__(self, token_service: TokenService, user_service: UserService) -> None:
        self._token_repo = token_service
        self._user_repo = user_service

    async def authenticate(self, token: str) -> User:
        user_id = await self._token_repo.get_user_id_by_token(token=token)
        if not user_id:
            raise UnauthorizedError
        user = await self._user_repo.get(user_id)
        if not user:
            raise UserNotExistsError(user_id=user_id)
        return user
