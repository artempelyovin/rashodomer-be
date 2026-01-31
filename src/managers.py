from sqlalchemy.orm import Session

from db.models import User
from db.query import login_exists, get_user
from db.utils import fetch_one, save_and_flush, fetch_one_or_none
from errors import LoginAlreadyExist, UserNotFound


class UserManager:
    def __init__(self, session: Session):
        self.session = session

    def create_user(
        self, first_name: str, last_name: str, login: str, password: str
    ) -> User:
        login_exist_ = fetch_one(session=self.session, query=login_exists(login=login))
        if login_exist_:
            raise LoginAlreadyExist(login=login)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            login=login,
            password_hash=password,
        )
        saved_user = save_and_flush(session=self.session, obj=new_user)
        return saved_user

    def get_user(self, user_id: str) -> User:
        user = fetch_one_or_none(session=self.session, query=get_user(user_id=user_id))
        if not user:
            raise UserNotFound(user_id=user_id)
        return user
