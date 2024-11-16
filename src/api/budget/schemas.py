from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel

IdField = Field(..., description="Unique ID of the budget")
NameField = Field(..., description="The name of the budget", examples=["Cash"])
DescriptionField = Field(
    ...,
    description="The description of the budget",
    examples=["A budget for tracking all cash transactions and managing daily expenses"],
)
AmountField = Field(..., description="The amount of the budget", examples=[42200])
UserIDField = Field(..., description="ID of user who created this budget")


class CreateBudgetSchema(FromAttributeModel):
    name: str = NameField
    description: str = DescriptionField
    amount: float = AmountField


class UpdateBudgetSchema(FromAttributeModel):
    name: str | None = Field(None, description="New name of the budget")
    description: str | None = Field(None, description="New description of the budget")
    amount: float | None = Field(None, description="New amount of the budget")


class BudgetSchema(FromAttributeModel):
    id: Annotated[str, UUID] = IdField
    name: str = NameField
    description: str = DescriptionField
    amount: float = AmountField
    user_id: str = UserIDField
