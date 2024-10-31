from src.core.entities import User
from src.core.exceptions import LoginAlreadyExistsError
from src.core.repositories import UserRepository
from src.core.services import PasswordService


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService) -> None:
        self._user_repo = user_repository
        self._password_service = password_service

    def register(self, first_name: str, last_name: str, login: str, password: str) -> User:
        user = self._user_repo.find_by_login(login=login)
        if user:
            raise LoginAlreadyExistsError
        password_hash = self._password_service.hash_password(password)
        return self._user_repo.create(
            first_name=first_name, last_name=last_name, login=login, password_hash=password_hash
        )
