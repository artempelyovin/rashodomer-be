import pytest
from faker import Faker

from enums import CategoryType
from managers.auth import AuthManager
from models import BudgetSchema, CategorySchema, DetailedUserSchema

fake = Faker(locale="ru_RU")


@pytest.fixture
def fake_budget() -> BudgetSchema:
    return BudgetSchema(
        name=fake.word(),
        description=fake.sentence(),
        amount=fake.pyfloat(positive=True),
        user_id=str(fake.uuid4()),
    )


@pytest.fixture
def fake_user() -> DetailedUserSchema:
    password = fake.password()
    password_hash = AuthManager.hash_password(password)
    return DetailedUserSchema(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        login=fake.user_name(),
        password_hash=password_hash,
        created_at=fake.date_time(),
        last_login=fake.date_time(),
    )


@pytest.fixture
def fake_category() -> CategorySchema:
    return CategorySchema(
        name=fake.word(),
        description=fake.sentence(),
        type=fake.random_element(list(CategoryType)),
        emoji_icon=fake.random_element([None, fake.emoji()]),
        is_archived=fake.boolean(),
        user_id=str(fake.uuid4()),
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )
