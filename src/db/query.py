from sqlalchemy import Select, select, exists

from db.models import User


def login_exists(login: str) -> Select[tuple[bool]]:
    return select(exists().where(User.login == login))


def list_users(limit: int | None = None, offset: int = 0) -> Select[tuple[User]]:
    return select(User).limit(limit).offset(offset)
