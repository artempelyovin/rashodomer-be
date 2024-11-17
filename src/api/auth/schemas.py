from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from api.base import FromAttributeModel

IdDesc = "UUnique ID of the user"
IdExamples = ["14a24fec-24a1-4b08-bd19-c77f02470da0"]
FirstNameDesc = "User's first name for personalization"
FirstNameExamples = ["Ivan"]
LastNameDesc = "User's last name for identification"
LastNameExamples = ["Ivanov"]
LoginDesc = "Unique username for system login"
LoginExamples = ["ivan-ivanov"]
PasswordDesc = "User's password; should be complex for security"
PasswordExamples = ["qwerty123456"]
CreatedAtDesc = "Date when user was created"
LastLoginDesc = "Date when user was last login"


class CreateUserSchema(FromAttributeModel):
    first_name: str = Field(..., description=FirstNameDesc, examples=FirstNameExamples)
    last_name: str = Field(..., description=LastNameDesc, examples=LastNameExamples)
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    password: str = Field(..., description=PasswordDesc, examples=PasswordExamples)


class UserLoginSchema(FromAttributeModel):
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    password: str = Field(..., description=PasswordDesc, examples=PasswordExamples)


class TokenSchema(FromAttributeModel):
    token: str = Field(..., description="Authentication token", examples=["2ba2eb37-7c80-49d0-8ff1-9f66cf6e977e"])


class UserSchema(FromAttributeModel):
    id: Annotated[str, UUID] = Field(..., description=IdDesc, examples=IdExamples)
    first_name: str = Field(..., description=FirstNameDesc, examples=FirstNameExamples)
    last_name: str = Field(..., description=LastNameDesc, examples=LastNameExamples)
    login: str = Field(..., description=LoginDesc, examples=LoginExamples)
    created_at: datetime = Field(..., description=CreatedAtDesc)
    last_login: datetime = Field(..., description=LastLoginDesc)
