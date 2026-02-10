from sqlalchemy.orm import Session

from db.models import User, Budget
from db.query import login_exists, get_user, budget_exists, get_user_by_login
from db.utils import fetch_one, save_and_flush, fetch_one_or_none
from errors import (
    LoginAlreadyExist,
    UserNotFound,
    BudgetAlreadyExist,
    AmountMustBePositive,
    Unauthorized,
)


def auth(session: Session) -> User:
    # TODO: tmp logic!!!
    user = fetch_one_or_none(
        session=session, query=get_user_by_login(login="test_user")
    )
    if user is None:
        raise Unauthorized
    return user


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


class BudgetManager:
    def __init__(self, session: Session):
        self.session = session
        self.user_manager = UserManager(session=session)

    def create_budget(
        self, user_id: str, name: str, description: str | None, amount: float
    ) -> Budget:
        if amount < 0:
            raise AmountMustBePositive
        budget_exists_ = fetch_one(
            session=self.session, query=budget_exists(name=name, user_id=user_id)
        )
        if budget_exists_:
            raise BudgetAlreadyExist(name=name)
        budget = Budget(
            user_id=user_id, name=name, description=description, amount=amount
        )
        save_and_flush(session=self.session, obj=budget)
        return budget
