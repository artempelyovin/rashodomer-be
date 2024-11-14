from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.budget.router import router as budget_router
from api.exception_handlers import core_exception_handler
from core.exceptions import BaseCoreError

fast_api = FastAPI()
fast_api.include_router(auth_router)
fast_api.include_router(budget_router)
fast_api.add_exception_handler(
    exc_class_or_status_code=BaseCoreError,
    handler=core_exception_handler,  # type: ignore[arg-type]
)
