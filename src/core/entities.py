from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from core.enums import CategoryType


class User(BaseModel):
    id: Annotated[str, UUID]
    first_name: str
    last_name: str
    login: str
    password_hash: str
    created_at: datetime
    last_login: datetime


class Budget(BaseModel):
    id: Annotated[str, UUID]
    name: str
    description: str | None
    amount: float
    user_id: Annotated[str, UUID]


class Category(BaseModel):
    id: Annotated[str, UUID]
    name: str
    description: str | None
    type: CategoryType
    is_archived: bool = False
    user_id: Annotated[str, UUID]
    created_at: datetime
    updated_at: datetime


class Expense(BaseModel):
    id: Annotated[str, UUID]
    amount: float
    description: str | None
    category_id: Annotated[str, UUID]
    user_id: Annotated[str, UUID]
    timestamp: datetime


class Income(BaseModel):
    id: Annotated[str, UUID]
    amount: float
    description: str | None
    category_id: Annotated[str, UUID]
    user_id: Annotated[str, UUID]
    timestamp: datetime
