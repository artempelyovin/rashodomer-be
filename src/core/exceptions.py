from core.utils import _


class BaseError(Exception):
    message: str | None = None

    def __init__(self, message: str | None = None) -> None:
        if message:
            super().__init__(message)
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
    def __init__(self, password_length: int) -> None:
        super().__init__(
            _("Password is too short. It must be at least {password_length} characters long").format(
                password_length=password_length
            )
        )


class PasswordMissingSpecialCharacterError(BaseError):
    message: str = _("Password is missing special character")
