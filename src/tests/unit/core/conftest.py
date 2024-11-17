import pytest
from faker import Faker

from core.entities import Budget, Category, Transaction, User
from core.enums import TransactionType

fake = Faker(locale="ru_RU")


@pytest.fixture
def fake_budget() -> Budget:
    return Budget(
        name=fake.word(),
        description=fake.sentence(),
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


@pytest.fixture
def fake_category() -> Category:
    return Category(
        name=fake.word(),
        description=fake.sentence(),
        type=fake.random_element(list(TransactionType)),
        emoji_icon=fake.random_element([None, fake.emoji()]),
        is_archived=fake.boolean(),
        user_id=str(fake.uuid4()),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )


@pytest.fixture
def fake_transaction() -> Transaction:
    return Transaction(
        amount=fake.pyfloat(positive=True),
        description=fake.sentence(),
        type=fake.random_element(list(TransactionType)),
        budget_id=str(fake.uuid4()),
        category_id=str(fake.uuid4()),
        user_id=str(fake.uuid4()),
        timestamp=fake.date_time(),
    )
