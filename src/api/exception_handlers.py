from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.exceptions import (
    BaseCoreError,
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
)

CORE_ERROR_TO_HTTP_STATUS_MAPPING: dict[type[BaseCoreError], int] = {
    LoginAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
    LoginNotExistsError: status.HTTP_404_NOT_FOUND,
    IncorrectPasswordError: status.HTTP_400_BAD_REQUEST,
    PasswordTooShortError: status.HTTP_400_BAD_REQUEST,
    PasswordMissingSpecialCharacterError: status.HTTP_400_BAD_REQUEST,
}


def core_exception_handler(request: Request, core_error: BaseCoreError) -> JSONResponse:  # noqa: ARG001
    status_code = CORE_ERROR_TO_HTTP_STATUS_MAPPING[type(core_error)]
    return JSONResponse(
        content={"content": None, "status_code": status_code, "error": True, "detailed": core_error.message()},
        status_code=status_code,
    )
