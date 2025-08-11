from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from exceptions import UnauthorizedError, UserNotExistsError
from managers.auth import AuthManager


NO_AUTH_PATHS = (
    '/login',
    '/register',
    '/_nicegui'  # needed for work nicegui
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
