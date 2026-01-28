# ruff: noqa: ARG001
from collections.abc import Generator
from pathlib import Path

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.testclient import TestClient

from app import fast_api
from depends import get_db
from enums import CategoryType
from repos.files import JsonFileMixin
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.transaction import TransactionSchema
from schemas.user import UserSchema
from tests.integration.utils import authenticate, create_budget, create_category, create_transaction, register
from db.engine import _engine

fake = Faker(locale="ru_RU")


@pytest.fixture
def client() -> TestClient:
    return TestClient(fast_api)


@pytest.fixture
async def db_session():
    async with _engine.connect() as conn:
        trans = await conn.begin()
        TestSessionMaker = async_sessionmaker(bind=conn, expire_on_commit=False)
        async with TestSessionMaker() as session:
            yield session
        await trans.rollback()


@pytest.fixture(autouse=True)
def override_db(client, db_session):
    async def _get_db():
        yield db_session

    fast_api.dependency_overrides[get_db] = _get_db


@pytest.fixture
def created_user(client: TestClient) -> UserSchema:
    login = fake.user_name()
    password = fake.password()
    user = register(
        client=client, first_name=fake.first_name(), last_name=fake.last_name(), login=login, password=password
    )
    token = authenticate(client=client, login=login, password=password)
    client.headers.update({"Authorization": token})  # <-- set global auth header
    return user


@pytest.fixture
def created_budget(client: TestClient, created_user: UserSchema) -> BudgetSchema:
    return create_budget(
        client=client,
        name=fake.word(),
        description=fake.sentence(),
        amount=fake.pyfloat(positive=True),
        emoji_icon=fake.random_element([None, fake.emoji()]),
    )


@pytest.fixture
def created_category(client: TestClient, created_user: UserSchema) -> CategorySchema:
    return create_category(
        client=client,
        name=fake.word(),
        description=fake.sentence(),
        category_type=fake.random_element(list(CategoryType)),
        emoji_icon=fake.random_element([None, fake.emoji()]),
    )


@pytest.fixture
def created_transaction(client: TestClient, created_category: CategorySchema) -> TransactionSchema:
    return create_transaction(
        client=client,
        amount=fake.pyfloat(positive=True),
        description=fake.sentence(),
        category_id=created_category.id,
        timestamp=fake.date_time_this_year(after_now=False),
    )


@pytest.fixture(autouse=True)
def remove_tmp_file() -> Generator[None, None, None]:
    """Run after each test and deletes the temporary database file"""
    yield  # run test
    # remove teardown
    tmp_file = Path(JsonFileMixin.filename)
    if tmp_file.exists():
        tmp_file.unlink()
