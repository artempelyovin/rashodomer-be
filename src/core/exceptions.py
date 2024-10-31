from src.core.utils import _


class BaseError(Exception):
    message: str | None = None

    def __init__(self, message: str) -> None:
        if message:
            super().__init__(self.message)
        elif self.message:
            super().__init__(self.message)


class LoginAlreadyExistsError(BaseError):
    def __init__(self, login: str) -> None:
        super().__init__(_('Login "{login}" already exists').format(login=login))


class LoginNotExistsError(BaseError):
    def __init__(self, login: str) -> None:
        super().__init__(_('Login "{login}" does not exist').format(login=login))


class IncorrectPasswordError(BaseError):
    message: str = _("Incorrect password")


class PasswordTooShortError(BaseError):
    message: str = _("Password is too short. It must be at least 8 characters long")


class PasswordMissingSpecialCharacterError(BaseError):
    message: str = _("Password is missing special character")
