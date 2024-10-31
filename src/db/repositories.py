from uuid import uuid4

from sqlalchemy import select

from core.entities import User
from db import Session
from db.models import UserModel


class UserRepository:
    @staticmethod
    async def create(first_name: str, last_name: str, login: str, password_hash: str) -> User:
        async with Session() as session:
            user = UserModel(
                id=uuid4(), first_name=first_name, last_name=last_name, login=login, password_hash=password_hash
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user.to_entity()

    @staticmethod
    async def find_by_login(login: str) -> User | None:
        async with Session() as session:
            query = select(UserModel).filter(UserModel.login == login)
            user = (await session.execute(query)).scalar_one_or_none()
            return user.to_entity() if user else None

    @staticmethod
    async def get(user_id: str) -> User | None:
        async with Session() as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            user = (await session.execute(query)).scalar_one_or_none()
            return user.to_entity() if user else None

    @staticmethod
    async def update_first_name(first_name: str) -> User:
        pass

    @staticmethod
    async def update_last_name(last_name: str) -> User:
        pass

    @staticmethod
    async def change_password(password: str) -> User:
        pass

    @staticmethod
    async def delete(user_id: str) -> None:
        pass
