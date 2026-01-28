from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://rashodomer:123456@localhost:5432/rashodomer-db"  # TODO: из настроек

_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # TODO: брать из настроек
    future=True,
)

_AsyncSessionMaker = async_sessionmaker(_engine, expire_on_commit=False, autocommit=False, autoflush=False)


async def get_session():
    async with _AsyncSessionMaker() as session:
        yield session
