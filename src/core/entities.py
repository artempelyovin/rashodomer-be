from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated
from uuid import UUID

from core.enums import CategoryType
from core.utils import uuid4_str


@dataclass
class User:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    first_name: str  # type: ignore[misc]
    last_name: str  # type: ignore[misc]
    login: str  # type: ignore[misc]
    password_hash: str  # type: ignore[misc]
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    last_login: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class Budget:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    name: str  # type: ignore[misc]
    description: str  # type: ignore[misc]
    amount: float  # type: ignore[misc]
    user_id: str  # type: ignore[misc]


@dataclass
class Category:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    name: str  # type: ignore[misc]
    description: str  # type: ignore[misc]
    type: CategoryType  # type: ignore[misc]
    is_archived: bool = field(default=False, kw_only=True)
    user_id: Annotated[str, UUID]  # type: ignore[misc]
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default_factory=datetime.now, kw_only=True)


@dataclass
class Expense:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    amount: float  # type: ignore[misc]
    description: str  # type: ignore[misc]
    category_id: str  # type: ignore[misc]
    user_id: str  # type: ignore[misc]
    timestamp: datetime  # type: ignore[misc]


@dataclass
class Income:
    id: str = field(default_factory=uuid4_str, kw_only=True)
    amount: float  # type: ignore[misc]
    description: str  # type: ignore[misc]
    category_id: str  # type: ignore[misc]
    user_id: str  # type: ignore[misc]
    timestamp: datetime  # type: ignore[misc]
