from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.exceptions import (
    AmountMustBePositiveError,
    BaseCoreError,
    BudgetAlreadyExistsError,
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UserNotExistsError,
)

CORE_ERROR_TO_HTTP_STATUS_MAPPING: dict[type[BaseCoreError], int] = {
    LoginAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
    LoginNotExistsError: status.HTTP_404_NOT_FOUND,
    UserNotExistsError: status.HTTP_404_NOT_FOUND,
    IncorrectPasswordError: status.HTTP_400_BAD_REQUEST,
    PasswordTooShortError: status.HTTP_400_BAD_REQUEST,
    PasswordMissingSpecialCharacterError: status.HTTP_400_BAD_REQUEST,
    AmountMustBePositiveError: status.HTTP_400_BAD_REQUEST,
    BudgetAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
}


def core_exception_handler(_: Request, core_error: BaseCoreError) -> JSONResponse:
    status_code = CORE_ERROR_TO_HTTP_STATUS_MAPPING[type(core_error)]
    return JSONResponse(
        content={"content": None, "status_code": status_code, "error": True, "detailed": core_error.message()},
        status_code=status_code,
    )
