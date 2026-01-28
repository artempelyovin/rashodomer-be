import string

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Token, User
from db.query.token import get_user_id_by_token
from db.query.user import get_user, find_user_by_login
from db.utils import fetch_one_or_none, save_and_flush
from exceptions import (
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UnauthorizedError,
    UserNotExistsError,
)
from schemas.user import CreateUserSchema, DetailedUserSchema
from utils import utc_now, uuid4_str


class AuthManager:  # TODO: переименовать в UserManager???
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_.decode()

    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    async def authenticate(self, token: str | None) -> DetailedUserSchema:
        if not token:
            raise UnauthorizedError
        user_id = await fetch_one_or_none(session=self.session, query=get_user_id_by_token(token))
        if not user_id:
            raise UnauthorizedError
        user = await fetch_one_or_none(session=self.session, query=get_user(user_id))
        if not user:
            raise UserNotExistsError(user_id=user_id)
        return DetailedUserSchema.model_validate(user, from_attributes=True)

    async def login(self, login: str, password: str) -> str:
        user = await fetch_one_or_none(session=self.session, query=find_user_by_login(login))
        if not user:
            raise LoginNotExistsError(login=login)
        if not self.check_password(password=password, password_hash=user.password_hash):
            raise IncorrectPasswordError
        new_token = Token(user_id=user.id, token=uuid4_str())
        self.session.add(new_token)
        user.last_login = utc_now()
        await self.session.commit()
        return new_token.token

    async def register(self, data: CreateUserSchema) -> DetailedUserSchema:
        user = await fetch_one_or_none(session=self.session, query=find_user_by_login(data.login))
        if user:
            raise LoginAlreadyExistsError(login=data.login)
        self._validate_password(data.password)
        password_hash = self.hash_password(data.password)
        user = User(first_name=data.first_name, last_name=data.last_name, login=data.login, password_hash=password_hash)
        saved_user = await save_and_flush(session=self.session, obj=user)
        await self.session.commit()
        return DetailedUserSchema.model_validate(saved_user, from_attributes=True)

    @classmethod
    def _validate_password(cls, password: str) -> None:
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            raise PasswordTooShortError(password_length=cls.MIN_PASSWORD_LENGTH)
        if not cls._has_special_characters(password):
            raise PasswordMissingSpecialCharacterError

    @staticmethod
    def _has_special_characters(password: str) -> bool:
        return any(char in string.punctuation for char in password)
