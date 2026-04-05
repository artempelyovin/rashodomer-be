from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from domain.utils import utc_now


class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


@dataclass
class Transaction:
    id: str
    budget_id: str
    category_id: str
    amount: Decimal
    type: TransactionType
    user_id: str
    date: datetime = field(default_factory=utc_now)
    description: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
