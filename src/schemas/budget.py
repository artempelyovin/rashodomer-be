from datetime import datetime
from typing import Annotated

from pydantic import AwareDatetime, Field

from base import CustomModel
from utils import UUID4Str, utc_now, uuid4_str

IdDesc = "Unique ID of the budget"
NameDesc = "The name of the budget"
NameExamples = ["Cash"]
DescriptionDesc = "The description of the budget"
DescriptionExamples = ["A budget for tracking all cash transactions and managing daily expenses"]
AmountDesc = "The amount of the budget"
AmountExamples = [42200]
EmojiIconDesc = "Emoji icon"
EmojiExamples = ["💵"]
UserIDDesc = "ID of user who created this budget"
CreatedAtDesc = "Date when budget was created"
UpdatedAtDesc = "Date when budget was updated"


class BudgetSchema(CustomModel):
    id: UUID4Str = Field(default_factory=uuid4_str, description=IdDesc)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(..., description=AmountDesc, examples=AmountExamples)
    emoji_icon: str | None = Field(..., description=EmojiIconDesc, examples=EmojiExamples)
    user_id: UUID4Str = Field(..., description=UserIDDesc)
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=CreatedAtDesc)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=UpdatedAtDesc)


class CreateBudgetSchema(CustomModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    amount: float = Field(0.0, description=AmountDesc, examples=AmountExamples)
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class UpdateBudgetSchema(CustomModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    amount: float | None = Field(None, description=AmountDesc, examples=AmountExamples)
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)
