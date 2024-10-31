from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

engine = AsyncEngine(
    create_engine(
        "postgresql+asyncpg://admin:123456@localhost:5432/rashodomer",  # TODO: remove hardcode
        echo=True,
    )
)
Session = async_sessionmaker(engine)
