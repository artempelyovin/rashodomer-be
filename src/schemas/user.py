from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from base import CustomModel
from utils import utc_now, uuid4_str

IdDesc = "Unique ID of the user"
FirstNameDesc = "User's first name for personalization"
FirstNameExamples = ["Ivan"]
LastNameDesc = "User's last name for identification"
LastNameExamples = ["Ivanov"]
LoginDesc = "Unique username for system login"
LoginExamples = ["ivan-ivanov"]
PasswordDesc = "User's password; should be complex for security"
PasswordExamples = ["qwerty123456"]
PasswordHashDesc = "Unique password hash"
PasswordHashExamples = ["$2b$12$0lsc7atrzcRHKmEisi/NIOUH/Sera2fNCv7lRzoAJ76gb9n3sE2fO"]
CreatedAtDesc = "Date when user was created"
LastLoginDesc = "Date when user was last login"


class UserSchema(CustomModel):
    id: Annotated[str, UUID] = Field(default_factory=uuid4_str, description=IdDesc)
    first_name: str = Field(..., description=FirstNameDesc, examples=FirstNameExamples)
    last_name: str = Field(..., description=LastNameDesc, examples=LastNameExamples)
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    created_at: datetime = Field(default_factory=utc_now, description=CreatedAtDesc)
    last_login: datetime = Field(default_factory=utc_now, description=LastLoginDesc)


class DetailedUserSchema(UserSchema):
    password_hash: str = Field(..., description=PasswordHashDesc, examples=PasswordHashExamples)


class CreateUserSchema(CustomModel):
    first_name: str = Field(..., description=FirstNameDesc, examples=FirstNameExamples)
    last_name: str = Field(..., description=LastNameDesc, examples=LastNameExamples)
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    password: str = Field(..., description=PasswordDesc, examples=PasswordExamples)


class UserLoginSchema(CustomModel):
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    password: str = Field(..., description=PasswordDesc, examples=PasswordExamples)


class TokenSchema(CustomModel):
    token: str = Field(..., description="Authentication token", examples=["2ba2eb37-7c80-49d0-8ff1-9f66cf6e977e"])
