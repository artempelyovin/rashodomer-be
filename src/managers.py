from sqlalchemy.orm import Session

from db.models import User
from db.query import login_exists
from db.utils import fetch_one, save_and_flush
from errors import LoginAlreadyExist


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
