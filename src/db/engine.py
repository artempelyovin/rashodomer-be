from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"  # TODO: из настроек

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # TODO: брать из настроек
    future=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
