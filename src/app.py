from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from base import ErrorSchema
from exceptions import BaseCoreError
from routers.auth import router as auth_router
from routers.budget import router as budget_router
from routers.category import router as category_router
from routers.transaction import router as transaction_router
from utils import get_version


def exception_handler(_: Request, core_error: BaseCoreError) -> JSONResponse:
    content = ErrorSchema.model_validate(
        {
            "type": core_error.__class__.__name__,
            "detail": core_error.message(),
        }
    ).model_dump(mode="json")
    return JSONResponse(content=content, status_code=core_error.status_code)


fast_api = FastAPI(version=get_version())
fast_api.include_router(auth_router)
fast_api.include_router(budget_router)
fast_api.include_router(category_router)
fast_api.include_router(transaction_router)
fast_api.add_exception_handler(
    exc_class_or_status_code=BaseCoreError,
    handler=exception_handler,  # type: ignore[arg-type]
)
fast_api.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=fast_api, host="127.0.0.1", port=8000)
