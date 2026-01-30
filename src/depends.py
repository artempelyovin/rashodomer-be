from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_session
from managers.auth import AuthManager
from repos.abc import (
    CategoryRepo,
    TokenRepo,
    TransactionRepo,
    UserRepo,
)
from repos.files import (
    FileCategoryRepo,
    FileTokenRepo,
    FileTransactionRepo,
    FileUserRepo,
)
from schemas.user import DetailedUserSchema

header_scheme = APIKeyHeader(
    name="Authorization", auto_error=False, description='Token in format: "Authorization": "{TOKEN}"'
)


def token_repo_factory() -> TokenRepo:
    return FileTokenRepo()


def user_repo_factory() -> UserRepo:
    return FileUserRepo()


def category_repo_factory() -> CategoryRepo:
    return FileCategoryRepo()


def transaction_repo_factory() -> TransactionRepo:
    return FileTransactionRepo()


async def authentication_user(token: Annotated[str | None, Depends(header_scheme)]) -> DetailedUserSchema:
    return await AuthManager.authenticate(token=token)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session
