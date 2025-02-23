from abc import ABC, abstractmethod
from dataclasses import dataclass

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from enums import CategoryType
from utils import _


class BaseCoreError(ABC, Exception):
    status_code: int

    @abstractmethod
    def message(self) -> str:
        pass

    def __str__(self) -> str:
        return self.message()


@dataclass(frozen=True)
class LoginAlreadyExistsError(BaseCoreError):
    login: str
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Login '{login}' already exists").format(login=self.login)


@dataclass(frozen=True)
class LoginNotExistsError(BaseCoreError):
    login: str
    status_code: int = HTTP_404_NOT_FOUND

    def message(self) -> str:
        return _("Login '{login}' does not exist").format(login=self.login)


@dataclass(frozen=True)
class UserNotExistsError(BaseCoreError):
    user_id: str
    status_code: int = HTTP_404_NOT_FOUND

    def message(self) -> str:
        return _("User with ID '{user_id}' does not exist").format(user_id=self.user_id)


class IncorrectPasswordError(BaseCoreError):
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Incorrect password")


@dataclass(frozen=True)
class PasswordTooShortError(BaseCoreError):
    password_length: int
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Password is too short. It must be at least {password_length} characters long").format(
            password_length=self.password_length
        )


class PasswordMissingSpecialCharacterError(BaseCoreError):
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Password is missing special character")


class AmountMustBePositiveError(BaseCoreError):
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Amount must be positive")


@dataclass(frozen=True)
class BudgetAlreadyExistsError(BaseCoreError):
    name: str
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("A budget with the name '{name}' already exists").format(name=self.name)


@dataclass(frozen=True)
class BudgetNotExistsError(BaseCoreError):
    budget_id: str
    status_code: int = HTTP_404_NOT_FOUND

    def message(self) -> str:
        return _("Budget with ID '{budget_id}' does not exist").format(budget_id=self.budget_id)


class BudgetAccessDeniedError(BaseCoreError):
    status_code: int = HTTP_403_FORBIDDEN

    def message(self) -> str:
        return _("Attempt to access another user's budget")


class UnauthorizedError(BaseCoreError):
    status_code: int = HTTP_403_FORBIDDEN

    def message(self) -> str:
        return _("Authentication failed")


class EmptySearchTextError(BaseCoreError):
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Search text cannot be empty")


class EmptyCategoryNameError(BaseCoreError):
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("Category name cannot be empty")


@dataclass(frozen=True)
class NotEmojiIconError(BaseCoreError):
    emoji_icon: str
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("The provided icon in text format '{emoji_icon}' is not a valid emoji").format(
            emoji_icon=self.emoji_icon
        )


@dataclass(frozen=True)
class CategoryAlreadyExistsError(BaseCoreError):
    name: str
    category_type: CategoryType
    status_code: int = HTTP_400_BAD_REQUEST

    def message(self) -> str:
        return _("A category with the name '{name}' and type '{category_type}' already exists").format(
            name=self.name, category_type=self.category_type
        )


@dataclass(frozen=True)
class CategoryNotExistsError(BaseCoreError):
    category_id: str
    status_code: int = HTTP_404_NOT_FOUND

    def message(self) -> str:
        return _("Category with ID '{category_id}' does not exist").format(category_id=self.category_id)


class CategoryAccessDeniedError(BaseCoreError):
    status_code: int = HTTP_403_FORBIDDEN

    def message(self) -> str:
        return _("Attempt to access another user's category")
