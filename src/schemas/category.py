from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AwareDatetime, Field

from base import CustomModel
from enums import CategoryType
from utils import utc_now, uuid4_str

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


class CategorySchema(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str, description=UserIDDesc)
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field(..., description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType = Field(..., description=CategoryTypeDesc, examples=CategoryTypeExamples)
    emoji_icon: str | None = Field(..., description=EmojiIconDesc, examples=EmojiExamples)
    is_archived: bool = Field(False, description=IsArchivedDesc)  # noqa: FBT003
    user_id: Annotated[str, UUID] = Field(..., description=UserIDDesc)
    created_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=CreatedAtDesc)
    updated_at: Annotated[datetime, AwareDatetime] = Field(default_factory=utc_now, description=UpdatedAtDesc)


class CreateCategorySchema(CustomModel):
    name: str = Field(..., description=NameDesc, examples=NameExamples)
    description: str = Field("", description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType = Field(..., description=CategoryTypeDesc, examples=CategoryTypeExamples)
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)


class UpdateCategorySchema(CustomModel):
    name: str | None = Field(None, description=NameDesc, examples=NameExamples)
    description: str | None = Field(None, description=DescriptionDesc, examples=DescriptionExamples)
    type: CategoryType | None = Field(None, description=CategoryTypeDesc, examples=CategoryTypeExamples)
    is_archived: bool | None = Field(False, description=IsArchivedDesc)  # noqa: FBT003
    emoji_icon: str | None = Field(None, description=EmojiIconDesc, examples=EmojiExamples)
