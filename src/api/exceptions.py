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
    CategoryAlreadyExistsError,
    EmptyBudgetTextError,
    EmptyCategoryNameError,
    IncorrectPasswordError,
    LoginAlreadyExistsError,
    LoginNotExistsError,
    NotEmojiIconError,
    PasswordMissingSpecialCharacterError,
    PasswordTooShortError,
    UnauthorizedError,
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
    BudgetNotExistsError: status.HTTP_404_NOT_FOUND,
    BudgetAccessDeniedError: status.HTTP_403_FORBIDDEN,
    UnauthorizedError: status.HTTP_403_FORBIDDEN,
    EmptyBudgetTextError: status.HTTP_400_BAD_REQUEST,
    EmptyCategoryNameError: status.HTTP_400_BAD_REQUEST,
    NotEmojiIconError: status.HTTP_400_BAD_REQUEST,
    CategoryAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
}


def core_exception_handler(_: Request, core_error: BaseCoreError) -> JSONResponse:
    status_code = CORE_ERROR_TO_HTTP_STATUS_MAPPING[type(core_error)]
    content = APIResponse.model_validate(
        {
            "result": None,
            "status_code": status_code,
            "error": {
                "type": core_error.__class__.__name__,
                "detail": core_error.message(),
            },
        }
    ).dict()
    return JSONResponse(content=content, status_code=status_code)
