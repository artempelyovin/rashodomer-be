from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from core.enums import CategoryType


class User(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    login: str
    password_hash: str
    created_at: datetime
    last_activity: datetime


class Budget(BaseModel):
    id: UUID
    name: str
    description: str | None
    amount: float
    user_id: UUID


class Category(BaseModel):
    id: UUID
    name: str
    description: str | None
    type: CategoryType
    is_archived: bool = False
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class Expense(BaseModel):
    id: UUID
    amount: float
    description: str | None
    category_id: UUID
    user_id: UUID
    timestamp: datetime


class Income(BaseModel):
    id: UUID
    amount: float
    description: str | None
    category_id: UUID
    user_id: UUID
    timestamp: datetime
