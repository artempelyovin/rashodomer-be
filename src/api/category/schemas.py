from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel
from core.enums import CategoryType

IdDesc = "Unique ID of the category"
NameDesc = description = "The name of the category"
NameExamples = ["Groceries"]
DescriptionDesc = "The description of the category"
DescriptionExamples = ["Products purchased in grocery stores"]
CategoryTypeDesc = "The type of category"
CategoryTypeExamples = [CategoryType.EXPENSE]
EmojiIconDesc = "Emoji icon"
EmojiExamples = ["🥦"]
IsArchivedDesc = "Is the category archived?"
UserIDDesc = "ID of user who created this category"
CreatedAtDesc = "Date when category was created"
UpdatedAtDesc = "Date when category was updated"


class CreateCategorySchema(FromAttributeModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType = Field(..., description=CategoryTypeDesc, examples=CategoryTypeExamples)
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class UpdateCategorySchema(FromAttributeModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType | None = Field(None, description=CategoryTypeDesc, examples=CategoryTypeExamples)
    is_archived: bool | None = Field(None, description=IsArchivedDesc, examples=[True])
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class CategorySchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(..., description=UserIDDesc)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType = Field(..., description=CategoryTypeDesc, examples=CategoryTypeExamples)
    emoji_icon: str | None = Field(..., description=EmojiIconDesc, examples=EmojiExamples)
    is_archived: bool = Field(..., description=IsArchivedDesc, examples=[False])
    user_id: Annotated[str, UUID] = Field(..., description=UserIDDesc)
    created_at: datetime = Field(..., description=CreatedAtDesc)
    updated_at: datetime = Field(..., description=UpdatedAtDesc)
