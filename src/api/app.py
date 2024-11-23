from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.auth.router import router as auth_router
from api.budget.router import router as budget_router
from api.category.router import router as category_router
from api.exceptions import core_exception_handler
from core.exceptions import BaseCoreError

fast_api = FastAPI()
fast_api.include_router(auth_router)
fast_api.include_router(budget_router)
fast_api.include_router(category_router)
fast_api.add_exception_handler(
    exc_class_or_status_code=BaseCoreError,
    handler=core_exception_handler,  # type: ignore[arg-type]
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
