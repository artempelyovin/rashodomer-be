# ruff: noqa: B008
from fastapi import APIRouter, Depends
from starlette import status

from api.auth.schemas import CreateUserSchema, TokenSchema, UserLoginSchema, UserSchema
from api.base import APIResponse, write_response
from api.depends import password_service_factory, token_service_factory, user_service_factory
from core.services import PasswordService, TokenService, UserService
from core.use_cases.auth.login import LoginUserUseCase
from core.use_cases.auth.register import RegisterUserUseCase

router = APIRouter()


@router.post(
    "/v1/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Register a new user",
    tags=["auth"],
)
async def register(
    body: CreateUserSchema,
    *,
    user_service: UserService = Depends(user_service_factory),
    password_service: PasswordService = Depends(password_service_factory),
) -> APIResponse[UserSchema]:
    use_case = RegisterUserUseCase(user_service=user_service, password_service=password_service)
    user = await use_case.register(
        first_name=body.first_name, last_name=body.last_name, login=body.login, password=body.password
    )
    return write_response(result=user, schema=UserSchema, status_code=status.HTTP_201_CREATED)


@router.post(
    "/v1/login",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Login in an existing user",
    tags=["auth"],
)
async def login(
    body: UserLoginSchema,
    *,
    user_service: UserService = Depends(user_service_factory),
    password_service: PasswordService = Depends(password_service_factory),
    token_service: TokenService = Depends(token_service_factory),
) -> APIResponse[TokenSchema]:
    use_case = LoginUserUseCase(
        user_service=user_service, password_service=password_service, token_service=token_service
    )
    token = await use_case.login(login=body.login, password=body.password)
    return write_response(result={"token": token}, schema=TokenSchema, status_code=status.HTTP_200_OK)
