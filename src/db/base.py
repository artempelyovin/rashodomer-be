from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime

from utils import utc_now

DATABASE_URL = "postgresql+psycopg2://rashodomer:123456@localhost:5432/rashodomer-db"


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )


_engine = create_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)
_session_maker = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


@contextmanager
def get_session_managed():
    session = _session_maker()
    try:
        yield session
    finally:
        session.close()
