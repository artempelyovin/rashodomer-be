from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.base import APIResponse
from core.exceptions import (
    AmountMustBePositiveError,
    BaseCoreError,
    BudgetAccessDeniedError,
    BudgetAlreadyExistsError,
    BudgetNotExistsError,
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UserNotExistsError, UnauthorizedError,
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
    BudgetNotExistsError: status.HTTP_404_NOT_FOUND,
    BudgetAccessDeniedError: status.HTTP_403_FORBIDDEN,
    UnauthorizedError: status.HTTP_403_FORBIDDEN,
}


def core_exception_handler(_: Request, core_error: BaseCoreError) -> JSONResponse:
    status_code = CORE_ERROR_TO_HTTP_STATUS_MAPPING[type(core_error)]
    content = APIResponse(data=None, status_code=status_code, error=True, detail=core_error.message()).dict()
    return JSONResponse(content=content, status_code=status_code)