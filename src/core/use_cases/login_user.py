from src.core.entities import User
from src.core.exceptions import IncorrectPasswordError, LoginNotExistsError
from src.core.repositories import UserRepository
from src.core.services import PasswordService


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService) -> None:
        self._user_repo = user_repository
        self._password_service = password_service

    def login(self, login: str, password: str) -> User:
        user = self._user_repo.find_by_login(login=login)
        if not user:
            raise LoginNotExistsError
        password_hash = self._password_service.hash_password(password)
        if user.password_hash != password_hash:
            raise IncorrectPasswordError
        return user
