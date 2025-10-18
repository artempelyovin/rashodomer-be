from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from depends import token_repo_factory, user_repo_factory
from managers.auth import AuthManager
from repos.abc import TokenRepo, UserRepo
from schemas.user import CreateUserSchema, TokenSchema, UserLoginSchema, UserSchema

router = APIRouter()

AUTH_TAG = "auth"


@router.post(
    "/v1/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Register a new user",
    tags=[AUTH_TAG],
)
async def register(
    body: CreateUserSchema,
    *,
    user_repo: Annotated[UserRepo, Depends(user_repo_factory)],
    token_repo: Annotated[TokenRepo, Depends(token_repo_factory)],
) -> UserSchema:
    manager = AuthManager(user_repo=user_repo, token_repo=token_repo)
    return await manager.register(data=body)


@router.post(
    "/v1/login",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Login in an existing user",
    tags=[AUTH_TAG],
)
async def login(
    body: UserLoginSchema,
    *,
    user_repo: Annotated[UserRepo, Depends(user_repo_factory)],
    token_repo: Annotated[TokenRepo, Depends(token_repo_factory)],
) -> TokenSchema:
    manager = AuthManager(user_repo=user_repo, token_repo=token_repo)
    token = await manager.login(login=body.login, password=body.password)
    return TokenSchema(token=token)
