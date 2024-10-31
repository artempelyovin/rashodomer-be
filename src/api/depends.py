from core.services import PasswordService, UserService
from db.repositories import UserRepository
from services import PasswordBcryptService


def get_password_service() -> PasswordService:
    return PasswordBcryptService()


def get_user_service() -> UserService:
    return UserRepository()
