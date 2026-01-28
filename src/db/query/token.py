from sqlalchemy import Select, select

from db.models import Token


def get_user_id_by_token(token: str) -> Select[tuple[str]]:
    return select(Token.user_id).where(Token.token == token)
