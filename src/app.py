from typing import Generator

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from db.base import get_session_managed
from errors import BaseError
from managers import UserManager
from schemas import CreateUserSchema, UserSchema

app = FastAPI()


@app.exception_handler(BaseError)
async def base_error_handler(_: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": exc.__class__.__name__,
            "detail": exc.message(),
        },
    )


def get_db_session() -> Generator[Session, None, None]:
    with get_session_managed() as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise


@app.post("/v1/users")
def create_user(
    body: CreateUserSchema,
    *,
    session: Session = Depends(get_db_session),
) -> UserSchema:
    manager = UserManager(session=session)
    new_user = manager.create_user(
        first_name=body.first_name,
        last_name=body.last_name,
        login=body.login,
        password=body.password,
    )
    session.commit()
    return UserSchema.model_validate(new_user, from_attributes=True)


@app.get("/v1/users/{user_id}")
def get_user(
    user_id: str,
    *,
    session: Session = Depends(get_db_session),
) -> UserSchema:
    manager = UserManager(session=session)
    user = manager.get_user(user_id=user_id)
    return UserSchema.model_validate(user, from_attributes=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
