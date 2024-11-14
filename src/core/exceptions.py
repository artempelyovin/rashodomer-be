from abc import abstractmethod
from dataclasses import dataclass

from core.utils import _


@dataclass(frozen=True)
class BaseCoreError(Exception):
    @abstractmethod
    def message(self) -> str:
        pass


@dataclass(frozen=True)
class LoginAlreadyExistsError(BaseCoreError):
    login: str

    def message(self) -> str:
        return _("Login '{login}' already exists").format(login=self.login)


@dataclass(frozen=True)
class LoginNotExistsError(BaseCoreError):
    login: str

    def message(self) -> str:
        return _("Login '{login}' does not exist").format(login=self.login)


@dataclass(frozen=True)
class IncorrectPasswordError(BaseCoreError):
    def message(self) -> str:
        return _("Incorrect password")


@dataclass(frozen=True)
class PasswordTooShortError(BaseCoreError):
    password_length: int

    def message(self) -> str:
        return _("Password is too short. It must be at least {password_length} characters long").format(
            password_length=self.password_length
        )


@dataclass(frozen=True)
class PasswordMissingSpecialCharacterError(BaseCoreError):
    def message(self) -> str:
        return _("Password is missing special character")
