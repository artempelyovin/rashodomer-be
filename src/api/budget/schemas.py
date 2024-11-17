from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel

IdDesc = "Unique ID of the budget"
IdExamples = ["8388551f-4bea-4c74-94f4-3db7dc56f13f"]
NameDesc = "The name of the budget"
NameExamples = ["Cash"]
DescriptionDesc = "The description of the budget"
DescriptionExamples = ["A budget for tracking all cash transactions and managing daily expenses"]
AmountDesc = "The amount of the budget"
AmountExamples = [42200]
UserIDDesc = "ID of user who created this budget"
UserIDExamples = ["2543ec71-22d6-47ae-8a1e-9441d050f17e"]


class CreateBudgetSchema(FromAttributeModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(0.0, description=AmountDesc, examples=AmountExamples)


class UpdateBudgetSchema(FromAttributeModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    amount: float | None = Field(None, description=AmountDesc, examples=AmountExamples)


class BudgetSchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(..., description=UserIDDesc, examples=UserIDExamples)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    user_id: str = Field(..., description=UserIDDesc, examples=UserIDExamples)
