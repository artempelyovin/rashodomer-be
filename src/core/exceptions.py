from abc import abstractmethod
from dataclasses import dataclass

from core.utils import _


class BaseCoreError(Exception):
    @abstractmethod
    def message(self) -> str:
        pass

    def __str__(self) -> str:
        return self.message()


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
class UserNotExistsError(BaseCoreError):
    user_id: str

    def message(self) -> str:
        return _("User with ID '{user_id}' does not exist").format(user_id=self.user_id)


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


class PasswordMissingSpecialCharacterError(BaseCoreError):
    def message(self) -> str:
        return _("Password is missing special character")


class AmountMustBePositiveError(BaseCoreError):
    def message(self) -> str:
        return _("Amount must be positive")


@dataclass(frozen=True)
class BudgetAlreadyExistsError(BaseCoreError):
    name: str

    def message(self) -> str:
        return _("A budget with the name '{name}' already exists").format(name=self.name)


@dataclass(frozen=True)
class BudgetNotExistsError(BaseCoreError):
    budget_id: str

    def message(self) -> str:
        return _("Budget with ID '{budget_id}' does not exist").format(budget_id=self.budget_id)


class BudgetAccessDeniedError(BaseCoreError):
    def message(self) -> str:
        return _("Attempt to access another user's budget.")


class UnauthorizedError(BaseCoreError):
    def message(self) -> str:
        return _("Authentication failed")


class EmptyInputError(BaseCoreError):
    def message(self) -> str:
        return _("Input cannot be empty. Please provide a valid input")
