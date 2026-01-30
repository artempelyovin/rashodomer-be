from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://rashodomer:123456@localhost:5432/rashodomer-db"  # TODO: из настроек

_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # TODO: брать из настроек
    future=True,
)

_async_session_maker = async_sessionmaker(_engine, expire_on_commit=False, autocommit=False, autoflush=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
