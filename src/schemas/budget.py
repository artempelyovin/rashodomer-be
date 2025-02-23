from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field

from base import FromAttributeModel
from utils import uuid4_str

IdDesc = "Unique ID of the budget"
NameDesc = "The name of the budget"
NameExamples = ["Cash"]
DescriptionDesc = "The description of the budget"
DescriptionExamples = ["A budget for tracking all cash transactions and managing daily expenses"]
AmountDesc = "The amount of the budget"
AmountExamples = [42200]
UserIDDesc = "ID of user who created this budget"


class BudgetSchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str, description=IdDesc)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    user_id: Annotated[str, UUID] = Field(..., description=UserIDDesc)


class CreateBudgetSchema(FromAttributeModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(0.0, description=AmountDesc, examples=AmountExamples)


class UpdateBudgetSchema(FromAttributeModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    amount: float | None = Field(None, description=AmountDesc, examples=AmountExamples)
