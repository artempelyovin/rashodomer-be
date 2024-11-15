from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel

IdField = Field(..., description="Unique ID of the user")
FirstNameField = Field(..., examples=["Ivan"])
LastNameField = Field(..., examples=["Ivanov"])
LoginField = Field(..., examples=["ivan-ivanov"])
PasswordField = Field(..., examples=["qwerty123456"])


class CreateUserSchema(FromAttributeModel):
    first_name: str = FirstNameField
    last_name: str = LastNameField
    login: str = LoginField
    password: str = PasswordField


class UserLoginSchema(FromAttributeModel):
    login: str = LoginField
    password: str = PasswordField


class UserSchema(FromAttributeModel):
    id: Annotated[str, UUID] = IdField
    first_name: str = FirstNameField
    last_name: str = LastNameField
    login: str = LoginField
    created_at: datetime
    last_login: datetime
