import pytest
from faker import Faker

from core.entities import Budget, User

fake = Faker(locale="ru_RU")


@pytest.fixture
def fake_budget() -> Budget:
    return Budget(
        name=fake.catch_phrase(),
        description=fake.catch_phrase(),
        amount=fake.pyfloat(positive=True),
        user_id=str(fake.uuid4()),
    )


@pytest.fixture
def fake_user() -> User:
    return User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        login=fake.user_name(),
        password_hash=str(fake.uuid4()),
        created_at=fake.date_time(),
        last_login=fake.date_time(),
    )
