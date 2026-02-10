from abc import abstractmethod, ABC
from dataclasses import dataclass


class BaseError(ABC, Exception):
    status_code: int

    @abstractmethod
    def message(self) -> str:
        pass

    def __str__(self) -> str:
        return self.message()


@dataclass
class LoginAlreadyExist(BaseError):
    status_code = 400
    login: str

    def message(self) -> str:
        return f"Login {self.login} already exists"


@dataclass
class UserNotFound(BaseError):
    status_code = 404
    user_id: str

    def message(self) -> str:
        return f"User {self.user_id} not found"


class Unauthorized(BaseError):
    status_code = 401

    def message(self) -> str:
        return f"Unauthorized"


class AmountMustBePositive(BaseError):
    status_code = 400

    def message(self) -> str:
        return "Amount must be positive"


@dataclass
class BudgetAlreadyExist(BaseError):
    status_code = 400
    name: str

    def message(self) -> str:
        return f"Budget {self.name} already exists"
