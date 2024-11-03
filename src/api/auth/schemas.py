from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

FirstNameField = Field(..., examples=["Ivan"])
LastNameField = Field(..., examples=["Ivanov"])
LoginField = Field(..., examples=["ivan-ivanov"])
PasswordField = Field(..., examples=["qwerty123456"])


class UserRegistrationSchema(BaseModel):
    first_name: str = FirstNameField
    last_name: str = LastNameField
    login: str = LoginField
    password: str = PasswordField


class UserSchema(BaseModel):
    id: UUID
    first_name: str = FirstNameField
    last_name: str = LastNameField
    login: str = LoginField
    created_at: datetime
    last_login: datetime
