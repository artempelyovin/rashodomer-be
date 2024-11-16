from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel
from core.enums import CategoryType

IdField = Field(..., description="Unique ID of the category")
NameField = Field(..., description="The name of the category", examples=["Groceries"])
DescriptionField = Field(
    ..., description="The description of the category", examples=["Products purchased in grocery stores"]
)
CategoryTypeField = Field(..., description="The type of category", examples=[CategoryType.EXPENSE])
EmojiIconField = Field(None, description="Emoji icon", examples=["🥦"])
IsArchivedField = Field(..., description="Is the category archived?", examples=[False])
UserIDField = Field(..., description="ID of user who created this category")
CreatedAtField = Field(..., description="Date when category was created")
UpdatedAtField = Field(..., description="Date when category was updated")


class CreateCategorySchema(FromAttributeModel):
    name: str = NameField
    description: str = DescriptionField
    type: CategoryType = CategoryTypeField
    emoji_icon: str | None = EmojiIconField


class CategorySchema(FromAttributeModel):
    id: Annotated[str, UUID] = IdField
    name: str = NameField
    description: str = DescriptionField
    type: CategoryType = CategoryTypeField
    emoji_icon: str | None = EmojiIconField
    is_archived: bool = IsArchivedField
    user_id: Annotated[str, UUID] = UserIDField
    created_at: datetime = CreatedAtField
    updated_at: datetime = UpdatedAtField
