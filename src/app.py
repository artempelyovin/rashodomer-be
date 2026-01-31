import uvicorn
from fastapi import FastAPI
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


@app.post("/v1/users")
def create_user(body: CreateUserSchema) -> UserSchema:
    with get_session_managed() as session:
        manager = UserManager(session=session)
        new_user = manager.create_user(
            first_name=body.first_name,
            last_name=body.last_name,
            login=body.login,
            password=body.password,
        )
        session.commit()
    return UserSchema.model_validate(new_user, from_attributes=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
