from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from domain.utils import utc_now


@dataclass
class Budget:
    id: str
    name: str
    balance: Decimal
    user_id: str
    description: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
