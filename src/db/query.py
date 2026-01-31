from sqlalchemy import Select, select, exists

from db.models import User


def login_exists(login: str) -> Select[tuple[bool]]:
    return select(exists().where(User.login == login))


def get_user(user_id: str) -> Select[tuple[User]]:
    return select(User).where(User.id == user_id)
