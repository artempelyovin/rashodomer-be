import logging

from nicegui import app, ui

from settings import settings
from ui.middlewares import AuthMiddleware
from ui.pages.auth import router as auth_router
from ui.pages.budgets import router as budgets_router

if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    app.add_middleware(AuthMiddleware)
    app.include_router(auth_router)
    app.include_router(budgets_router)
    ui.run(storage_secret=settings.storage_secret.get_secret_value(), reload=True)
