import string

from core.entities import User
from core.exceptions import LoginAlreadyExistsError, PasswordMissingSpecialCharacterError, PasswordTooShortError
from core.services import PasswordService
from core.repos import UserRepository


class RegisterUserUseCase:
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, user_service: UserRepository, password_service: PasswordService) -> None:
        self._user_repo = user_service
        self._password_service = password_service

    async def register(self, first_name: str, last_name: str, login: str, password: str) -> User:
        user = await self._user_repo.find_by_login(login=login)
        if user:
            raise LoginAlreadyExistsError(login=login)
        self._validate_password(password)
        password_hash = self._password_service.hash_password(password)
        return await self._user_repo.create(
            first_name=first_name, last_name=last_name, login=login, password_hash=password_hash
        )

    def _validate_password(self, password: str) -> None:
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(password_length=self.MIN_PASSWORD_LENGTH)
        if not self._has_special_characters(password):
            raise PasswordMissingSpecialCharacterError

    @staticmethod
    def _has_special_characters(password: str) -> bool:
        return any(char in string.punctuation for char in password)
