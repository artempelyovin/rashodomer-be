from datetime import datetime

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    login: str
    password: str


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    login: str
    password_hash: str
    last_login: datetime
    created_at: datetime
    updated_at: datetime
