from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AwareDatetime, Field

from base import CustomModel
from utils import utc_now, uuid4_str

IdDesc = "Unique ID of the transaction"
AmountDesc = "The amount of the transaction"
AmountExamples = [150]
DescriptionDesc = "The description of the transaction"
DescriptionExamples = ["Going to the grocery store"]
CategoryIdDesc = "ID of the category in which the transaction was made"
UserIDDesc = "ID of user who created this transaction"
TimestampDesc = "Date when the transaction was completed"
CreatedAtDesc = "Date when transaction was created"
UpdatedAtDesc = "Date when transaction was updated"


class TransactionSchema(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str, description=IdDesc)
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    category_id: Annotated[str, UUID] = Field(..., description=CategoryIdDesc)
    user_id: Annotated[str, UUID] = Field(..., description=UserIDDesc)
    timestamp: Annotated[datetime, AwareDatetime] = Field(..., description=TimestampDesc)
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=CreatedAtDesc)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=CreatedAtDesc)


class CreateTransactionSchema(CustomModel):
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    category_id: Annotated[str, UUID] = Field(..., description=CategoryIdDesc)
    timestamp: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=TimestampDesc)


class UpdateTransactionSchema(CustomModel):
    amount: float | None = Field(None, description=AmountDesc, examples=AmountExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    category_id: Annotated[str, UUID] | None = Field(None, description=CategoryIdDesc)
    timestamp: Annotated[datetime, AwareDatetime] | None = Field(None, description=TimestampDesc)
