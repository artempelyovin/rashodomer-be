import logging

from nicegui import APIRouter, app, ui
from nicegui.elements.input import Input

from exceptions import IncorrectPasswordError, LoginNotExistsError
from managers.auth import AuthManager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.page("/login")
async def login(unauthorized: bool = False):
    async def validate_and_login(login: Input, password: Input):
        if not login.value:
            return ui.notify("Заполните логин", type="negative")
        if not password.value:
            return ui.notify("Заполните пароль", type="negative")

        try:
            token = await AuthManager().login(login.value, password.value)
        except (LoginNotExistsError, IncorrectPasswordError):
            ui.notify("Неверный логин или пароль", type="negative")
            password.value = ""
            return
        app.storage.user["token"] = token
        ui.navigate.to("/budgets")

    logger.info(f"Show /login for user {ui.context.client.id} ({ui.context.client.ip})")
    if unauthorized:
        ui.notify("Не авторизован", type="negative")
    login = ui.input("Логин", value="ivan-ivanov").classes("w-1/6")  # TODO: убери default value
    password = ui.input("Пароль", value="qwerty123456@", password=True, password_toggle_button=True).classes(
        "w-1/6"
    )  # TODO: убери default value
    ui.button("Войти", on_click=lambda _: validate_and_login(login, password))
