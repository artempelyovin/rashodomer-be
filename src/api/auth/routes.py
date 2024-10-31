from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.auth.schemas import UserRegistrationSchema, UserSchema
from api.depends import get_password_service, get_user_service
from core.services import PasswordService, UserService
from core.use_cases.register_user import RegisterUserUseCase

router = APIRouter()


@router.post(
    "/v1/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
    summary="Register user",
    description="Register a new user",
    tags=["auth"],
)
async def register(  # noqa: ANN201
    user_info: UserRegistrationSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
):
    register_use_case = RegisterUserUseCase(user_service=user_service, password_service=password_service)
    return await register_use_case.register(
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        login=user_info.login,
        password=user_info.password,
    )
