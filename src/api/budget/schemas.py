from typing import Annotated

from pydantic import UUID4, BaseModel, Field

IdField = Field(..., description="Unique ID of the budget")
NameField = Field(..., description="The name of the budget", examples=["Cash"])
DescriptionField = Field(
    ...,
    description="The description of the budget",
    examples=["A budget for tracking all cash transactions and managing daily expenses"],
)
AmountField = Field(..., description="The amount of the budget", examples=[42200])
UserIDField = Field(..., description="ID of user who created this budget")


class CreateBudgetSchema(BaseModel):
    name: str = NameField
    description: str = DescriptionField
    amount: float = AmountField
    user_id: Annotated[str, UUID4] = UserIDField


class BudgetSchema(BaseModel):
    id: Annotated[str, UUID4] = IdField
    name: str = NameField
    description: str = DescriptionField
    amount: float = AmountField
    user_id: str = UserIDField


BudgetListSchema = list[BudgetSchema]
