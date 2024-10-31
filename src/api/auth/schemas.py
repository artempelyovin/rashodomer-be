from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserRegistrationSchema(BaseModel):
    first_name: str = Field(..., examples=["Ivan"])
    last_name: str = Field(..., examples=["Ivanov"])
    login: str = Field(..., examples=["ivan-ivanov"])
    password: str = Field(..., examples=["qwerty123456"])


class UserSchema(BaseModel):
    id: UUID
    first_name: str = Field(..., examples=["Ivan"])
    last_name: str = Field(..., examples=["Ivanov"])
    login: str = Field(..., examples=["ivan-ivanov"])
    created_at: datetime
    last_activity: datetime
