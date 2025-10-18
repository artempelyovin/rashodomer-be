import logging

from nicegui import APIRouter, app, ui
from nicegui.elements.input import Input

from exceptions import BaseCoreError, IncorrectPasswordError, LoginAlreadyExistsError, LoginNotExistsError
from managers.auth import AuthManager
from models import CreateUserSchema

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
    login_ = ui.input("Логин").classes("w-1/6")  # TODO: убери default value
    password_ = ui.input("Пароль", password=True, password_toggle_button=True).classes("w-1/6")
    ui.button("Войти", on_click=lambda _: validate_and_login(login_, password_))


@router.page("/register")
async def register():
    async def validate_and_register(first_name: Input, last_name: Input, login: Input, password: Input):
        if not first_name.value:
            return ui.notify("Заполните имя", type="negative")
        if not last_name.value:
            return ui.notify("Заполните фамилию", type="negative")
        if not login.value:
            return ui.notify("Заполните логин", type="negative")
        if not password.value:
            return ui.notify("Заполните пароль", type="negative")
        try:
            await AuthManager().register(
                data=CreateUserSchema(
                    first_name=first_name.value, last_name=last_name.value, login=login.value, password=password.value
                )
            )
        except BaseCoreError as e:
            ui.notify(e.message(), type="negative")
            return

        logger.info(f"User ({first_name.value=}, {last_name_.value=}, {login_.value=}) registered successfully")
        ui.navigate.to("/login")

    first_name_ = ui.input("Имя")
    last_name_ = ui.input("Фамилия")
    login_ = ui.input("Логин")
    password_ = ui.input("Пароль", password=True, password_toggle_button=True)
    ui.button("Регистрация", on_click=lambda _: validate_and_register(first_name_, last_name_, login_, password_))
