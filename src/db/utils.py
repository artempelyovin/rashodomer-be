from typing import TypeVar

from sqlalchemy import Select

from sqlalchemy.orm import DeclarativeBase, Session

T = TypeVar("T")
M = TypeVar("M", bound=DeclarativeBase)


def fetch_one(session: Session, query: Select[tuple[T]]) -> T:
    result = session.execute(query)
    return result.scalars().one()


def fetch_one_or_none(session: Session, query: Select[tuple[T]]) -> T | None:
    result = session.execute(query)
    return result.scalars().one_or_none()


def fetch_all(session: Session, query: Select[T]) -> list[T]:
    result = session.execute(query)
    return list(result.scalars().all())


def save_and_flush(session: Session, obj: M) -> M:
    session.add(obj)
    session.flush()
    return obj
