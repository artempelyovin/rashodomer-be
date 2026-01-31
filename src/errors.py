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
