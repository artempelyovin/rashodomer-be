import random
from typing import Generator

import pytest
from faker import Faker
from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from app import app, get_db_session
from db.base import DATABASE_URL
from schemas import UserSchema, BudgetSchema
from tests import utils


@pytest.fixture(scope="session")
def faker():
    fake = Faker("ru_RU")
    Faker.seed(1500)  # for a deterministic state
    return fake


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    return create_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)


@pytest.fixture(scope="session")
def db_connection(db_engine: Engine) -> Generator[Connection, None, None]:
    connection = db_engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_session(db_connection: Connection) -> Generator[Session, None, None]:
    transaction = db_connection.begin_nested()
    session_factory = sessionmaker(bind=db_connection)
    session = session_factory()
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db_session] = _get_test_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def created_user(client, faker) -> UserSchema:
    return utils.create_user(
        client,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        login="test_user",  # TODO: tmp!!!
        password=faker.password(),
    )


@pytest.fixture
def created_budget(client, faker, created_user) -> BudgetSchema:
    return utils.create_budget(
        client,
        name=faker.bban(),
        description=random.choice([faker.text(), None]),
        amount=faker.pyfloat(min_value=0),
    )
