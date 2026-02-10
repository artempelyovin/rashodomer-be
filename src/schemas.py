from datetime import datetime

from pydantic import BaseModel, constr


class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    login: str
    password: str


class UserSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    login: str
    password_hash: str
    last_login: datetime
    created_at: datetime
    updated_at: datetime


class CreateBudgetSchema(BaseModel):
    name: constr(max_length=64)
    description: str | None = None
    amount: float = 0


class BudgetSchema(BaseModel):
    id: str
    user_id: str
    name: str
    description: str | None
    amount: float
    created_at: datetime
    updated_at: datetime
