import asyncio
from sqlalchemy import select

from db.engine import AsyncSessionLocal
from db.models import User


async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(users)


if __name__ == "__main__":
    asyncio.run(main())
