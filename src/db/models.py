from datetime import datetime

from sqlalchemy import UUID, DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.entities import User


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    login: Mapped[str] = mapped_column(String(64), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def to_entity(self) -> User:
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            login=self.login,
            password_hash=self.password_hash,
            created_at=self.created_at,
            last_activity=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserModel":
        return UserModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            login=user.login,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.last_activity,
        )
