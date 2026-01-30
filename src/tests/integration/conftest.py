# ruff: noqa: ARG001
from collections.abc import Generator
from pathlib import Path
from typing import AsyncGenerator

import pytest
from faker import Faker
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from starlette.testclient import TestClient

from app import fast_api
from db.engine import DATABASE_URL
from depends import get_async_session
from enums import CategoryType
from repos.files import JsonFileMixin
from schemas.budget import BudgetSchema
from schemas.category import CategorySchema
from schemas.transaction import TransactionSchema
from schemas.user import UserSchema
from tests.integration.utils import authenticate, create_budget, create_category, create_transaction, register

fake = Faker(locale="ru_RU")
engine = create_async_engine(DATABASE_URL, echo=True)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with engine.connect() as connection:
        transaction = await connection.begin()

        async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
            async with AsyncSession(bind=connection, expire_on_commit=False, autoflush=False) as session:
                await session.begin_nested()
                yield session

        fast_api.dependency_overrides[get_async_session] = get_session_override

        async with AsyncClient(transport=ASGITransport(app=fast_api), base_url="http://test") as client:
            yield client

        await transaction.rollback()
        fast_api.dependency_overrides.clear()


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
