from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.auth.schemas import CreateUserSchema, UserLoginSchema, UserSchema
from api.depends import password_service_factory, user_service_factory
from core.services import PasswordService, UserService
from core.use_cases.login_user import LoginUserUseCase
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
async def register(
    body: CreateUserSchema,
    user_service: Annotated[UserService, Depends(user_service_factory)],
    password_service: Annotated[PasswordService, Depends(password_service_factory)],
):
    use_case = RegisterUserUseCase(user_service=user_service, password_service=password_service)
    return await use_case.register(
        first_name=body.first_name, last_name=body.last_name, login=body.login, password=body.password
    )


@router.post(
    "/v1/login",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Login user",
    description="Login in an existing user",
    tags=["auth"],
)
async def login(
    body: UserLoginSchema,
    user_service: Annotated[UserService, Depends(user_service_factory)],
    password_service: Annotated[PasswordService, Depends(password_service_factory)],
):
    use_case = LoginUserUseCase(user_service=user_service, password_service=password_service)
    await use_case.login(login=body.login, password=body.password)
