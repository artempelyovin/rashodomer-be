from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated
from uuid import UUID

from core.enums import CategoryType
from core.utils import uuid4_str


@dataclass
class User:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    first_name: str
    last_name: str
    login: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    last_login: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class Budget:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    name: str
    description: str
    amount: float
    user_id: str


@dataclass
class Category:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    name: str
    description: str
    type: CategoryType
    is_archived: bool = field(default=False, kw_only=True)
    user_id: Annotated[str, UUID]
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class Expense:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    amount: float
    description: str
    category_id: str
    user_id: str
    timestamp: datetime


@dataclass
class Income:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    amount: float
    description: str
    category_id: str
    user_id: str
    timestamp: datetime
