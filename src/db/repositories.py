from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import select

from core.entities import User
from db import Session
from db.models import UserModel


class UserRepository:
    async def create(self, first_name: str, last_name: str, login: str, password_hash: str) -> User:
        async with Session() as session:
            user = UserModel(
                id=uuid4(), first_name=first_name, last_name=last_name, login=login, password_hash=password_hash
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user.to_entity()

    async def find_by_login(self, login: str) -> User | None:
        async with Session() as session:
            query = select(UserModel).filter(UserModel.login == login)
            user = (await session.execute(query)).scalar_one_or_none()
            return user.to_entity() if user else None

    async def get(self, user_id: str) -> User | None:
        async with Session() as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            user = (await session.execute(query)).scalar_one_or_none()
            return user.to_entity() if user else None

    async def update_first_name(self, user_id: str, first_name: str) -> User:
        return await self._update_attribute(user_id, "first_name", first_name)

    async def update_last_name(self, user_id: str, last_name: str) -> User:
        return await self._update_attribute(user_id, "last_name", last_name)

    async def update_last_login(self, user_id: str, last_login: datetime) -> User:
        return await self._update_attribute(user_id, "last_login", last_login)

    async def change_password(self, password: str) -> User:
        pass

    async def delete(self, user_id: str) -> None:
        pass

    @staticmethod
    async def _update_attribute(user_id: str, attribute: str, value: Any) -> User:
        async with Session() as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            user = (await session.execute(query)).scalar_one()
            setattr(user, attribute, value)
            await session.commit()
            await session.refresh(user)
            return user.to_entity()
