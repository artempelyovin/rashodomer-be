from sqlalchemy import Select, select, exists

from db.models import User, Budget


def login_exists(login: str) -> Select[tuple[bool]]:
    return select(exists().where(User.login == login))


def get_user(user_id: str) -> Select[tuple[User]]:
    return select(User).where(User.id == user_id)


def get_user_by_login(login: str) -> Select[tuple[User]]:
    return select(User).where(User.login == login)


def budget_exists(name: str, user_id: str) -> Select[tuple[bool]]:
    return select(exists().where(Budget.name == name).where(Budget.user_id == user_id))
