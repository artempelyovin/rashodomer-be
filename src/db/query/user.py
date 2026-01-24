from datetime import datetime

from sqlalchemy import select, update, delete, Update, Delete, Select

from db.models import User


def get_user(user_id: str) -> Select[tuple[User]]:
    return select(User).where(User.id == user_id)


def find_user_by_login(login: str) -> Select[tuple[User]]:
    return select(User).where(User.login == login)


def update_user_first_name(user_id: str, first_name: str) -> Update:
    return update(User).where(User.id == user_id).values(first_name=first_name).returning(User)


def update_user_last_name(user_id: str, last_name: str) -> Update:
    return update(User).where(User.id == user_id).values(last_name=last_name).returning(User)


def update_user_last_login(user_id: str, last_login: datetime) -> Update:
    return update(User).where(User.id == user_id).values(last_login=last_login).returning(User)


def change_user_password_hash(user_id: str, password_hash: str) -> Update:
    return update(User).where(User.id == user_id).values(password_hash=password_hash).returning(User)


def delete_user(user_id: str) -> Delete:
    return delete(User).where(User.id == user_id)
