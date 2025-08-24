from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from enums import CategoryType
from utils import utc_now, uuid4_str

ISO_TIMEZONE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class CustomModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime(ISO_TIMEZONE_FORMAT),  # all dates as ISO with TIMEZONE
        },
    )


class Budget(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str)
    name: str
    description: str
    amount: float
    user_id: Annotated[str, UUID]
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)


class Category(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str)
    name: str
    description: str
    type: CategoryType
    emoji_icon: str | None
    is_archived: bool = Field(False)
    user_id: Annotated[str, UUID]
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)


class Transaction(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str)
    amount: float
    description: str
    category_id: Annotated[str, UUID]
    user_id: Annotated[str, UUID]
    timestamp: Annotated[datetime, AwareDatetime]
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now)


class User(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str)
    first_name: str
    last_name: str
    login: str
    created_at: datetime = Field(default_factory=utc_now)
    last_login: datetime = Field(default_factory=utc_now)


class DetailedUser(User):
    password_hash: str


class CreateUser(CustomModel):
    first_name: str
    last_name: str
    login: str
    password: str


class Token(CustomModel):
    token: str
