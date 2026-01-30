from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from depends import get_async_session
from managers.auth import AuthManager
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
    session: AsyncSession = Depends(get_async_session),
) -> UserSchema:
    manager = AuthManager(session=session)
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
    session: AsyncSession = Depends(get_async_session),
) -> TokenSchema:
    manager = AuthManager(session=session)
    token = await manager.login(login=body.login, password=body.password)
    return TokenSchema(token=token)
