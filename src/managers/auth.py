import string
from datetime import UTC, datetime

import bcrypt

from exceptions import (
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UnauthorizedError,
    UserNotExistsError,
)
from models import CreateUser, DetailedUser
from repos.abc import TokenRepo, UserRepo
from settings import settings


class AuthManager:
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, user_repo: UserRepo = settings.user_repo, token_repo: TokenRepo = settings.token_repo) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo

    @staticmethod
    def hash_password(password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_.decode()

    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    async def authenticate(self, token: str | None) -> DetailedUser:
        if not token:
            raise UnauthorizedError
        user_id = await self.token_repo.get_user_id_by_token(token=token)
        if not user_id:
            raise UnauthorizedError
        user = await self.user_repo.get(user_id)
        if not user:
            raise UserNotExistsError(user_id=user_id)
        return user

    async def login(self, login: str, password: str) -> str:
        user = await self.user_repo.find_by_login(login=login)
        if not user:
            raise LoginNotExistsError(login=login)
        if not self.check_password(password=password, password_hash=user.password_hash):
            raise IncorrectPasswordError
        await self.user_repo.update_last_login(user_id=user.id, last_login=datetime.now(tz=UTC))
        return await self.token_repo.create_new_token(user_id=user.id)

    async def register(self, data: CreateUser) -> DetailedUser:
        user = await self.user_repo.find_by_login(login=data.login)
        if user:
            raise LoginAlreadyExistsError(login=data.login)
        self._validate_password(data.password)
        password_hash = self.hash_password(data.password)
        user = DetailedUser(
            first_name=data.first_name, last_name=data.last_name, login=data.login, password_hash=password_hash
        )
        return await self.user_repo.add(user)

    def _validate_password(self, password: str) -> None:
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(password_length=self.MIN_PASSWORD_LENGTH)
        if not self._has_special_characters(password):
            raise PasswordMissingSpecialCharacterError

    @staticmethod
    def _has_special_characters(password: str) -> bool:
        return any(char in string.punctuation for char in password)
