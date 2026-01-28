from typing import TypeVar

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T")
M = TypeVar("M", bound=DeclarativeBase)


async def fetch_one(session: AsyncSession, query: Select[tuple[T]]) -> T:
    result = await session.execute(query)
    return result.scalars().one()


async def fetch_one_or_none(session: AsyncSession, query: Select[tuple[T]]) -> T | None:
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def fetch_all(session: AsyncSession, query: Select[T]) -> list[T]:
    result = await session.execute(query)
    return list(result.scalars().all())


async def save_and_flush(session: AsyncSession, obj: M) -> M:
    session.add(obj)
    await session.flush()
    return obj
