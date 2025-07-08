from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from exceptions import UnauthorizedError, UserNotExistsError
from managers.auth import AuthManager


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path.startswith("/login"):
            return await call_next(request)

        try:
            user = await AuthManager().authenticate(token=app.storage.user.get("token"))
            request.state.user = user
            return await call_next(request)
        except (UnauthorizedError, UserNotExistsError):
            return RedirectResponse("/login?unauthorized=True")
