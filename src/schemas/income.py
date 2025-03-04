from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from utils import uuid4_str


class IncomeSchema(BaseModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str)
    amount: float
    description: str
    category_id: Annotated[str, UUID]
    user_id: Annotated[str, UUID]
    timestamp: datetime
