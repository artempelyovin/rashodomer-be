from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel
from core.enums import TransactionType

IdDesc = "Unique ID of the category"
IdExamples = ["31d1d9ec-a71a-4a40-bc7a-417f1b9b8701"]
NameDesc = description = "The name of the category"
NameExamples = ["Groceries"]
DescriptionDesc = "The description of the category"
DescriptionExamples = ["Products purchased in grocery stores"]
TransactionTypeDesc = "The category transaction type"
TransactionTypeExamples = [TransactionType.EXPENSE]
EmojiIconDesc = "Emoji icon"
EmojiExamples = ["🥦"]
IsArchivedDesc = "Is the category archived?"
UserIdDesc = "ID of user who created this category"
UserIdExamples = ["2543ec71-22d6-47ae-8a1e-9441d050f17e"]
CreatedAtDesc = "Date when category was created"
UpdatedAtDesc = "Date when category was updated"


class CreateCategorySchema(FromAttributeModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    type: TransactionType = Field(..., description=TransactionTypeDesc, examples=TransactionTypeExamples)
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class UpdateCategorySchema(FromAttributeModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    type: TransactionType | None = Field(None, description=TransactionTypeDesc, examples=TransactionTypeExamples)
    is_archived: bool | None = Field(None, description=IsArchivedDesc, examples=[True])
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class CategorySchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(..., description=UserIdDesc, examples=IdExamples)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    type: TransactionType = Field(..., description=TransactionTypeDesc, examples=TransactionTypeExamples)
    emoji_icon: str | None = Field(..., description=EmojiIconDesc, examples=EmojiExamples)
    is_archived: bool = Field(..., description=IsArchivedDesc, examples=[False])
    user_id: Annotated[str, UUID] = Field(..., description=UserIdDesc, examples=UserIdExamples)
    created_at: datetime = Field(..., description=CreatedAtDesc)
    updated_at: datetime = Field(..., description=UpdatedAtDesc)
