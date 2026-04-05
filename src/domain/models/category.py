from dataclasses import dataclass, field
from datetime import datetime

from domain.models.transaction import TransactionType
from domain.utils import utc_now


@dataclass
class Category:
    id: str
    name: str
    user_id: str
    transaction_type: TransactionType | None = None
    description: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
