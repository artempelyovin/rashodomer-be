import logging

from nicegui import app, ui
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from exceptions import BaseCoreError, UnauthorizedError, UserNotExistsError
from managers.auth import AuthManager

logger = logging.getLogger(__name__)

NO_AUTH_PATHS = (
    "/login",
    "/register",
    "/_nicegui",  # needed for work nicegui
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if any(request.url.path.startswith(path) for path in NO_AUTH_PATHS):
            return await call_next(request)

        try:
            user = await AuthManager().authenticate(token=app.storage.user.get("token"))
            request.state.user = user
            return await call_next(request)
        except (UnauthorizedError, UserNotExistsError):
            return RedirectResponse("/login?unauthorized=True", status_code=303)


def on_exception_handler(e: Exception) -> None:
    if isinstance(e, BaseCoreError):
        logger.error(e.message())
        ui.notify(e.message(), type="negative")
    else:
        logger.exception("Uncaught exception:")
        ui.notify("Упс... Что-то пошло не так", type="negative")
