from nicegui import APIRouter, ui
from starlette.requests import Request

from schemas.user import DetailedUserSchema
from ui.components.labels import id_with_copy
from utils import datetime_to_text

router = APIRouter()


@router.page("/me")
async def about_me(request: Request):
    user: DetailedUserSchema = request.state.user

    with ui.row():
        ui.button(icon="arrow_back", on_click=ui.navigate.back)
        ui.label("Обо мне").classes('')
    with ui.row():
        id_with_copy(user.id)
    with ui.row():
        ui.label("Имя:").classes('text-sm')
        ui.label(user.first_name)
    with ui.row():
        ui.label("Фамилия:").classes('text-sm')
        ui.label(user.last_name)
    with ui.row():
        ui.label("Логин:").classes('text-sm')
        ui.label(user.login)
    with ui.row():
        ui.label("Дата регистрации:").classes('text-sm')
        ui.label(datetime_to_text(user.created_at))
    with ui.row():
        ui.label("Последний заход:").classes('text-sm')
        ui.label(datetime_to_text(user.last_login))
