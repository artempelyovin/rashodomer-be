import gettext
import uuid
from datetime import UTC, datetime

_ = gettext.gettext


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def datetime_to_text(datetime_: datetime) -> str:
    return datetime_.strftime("%Y-%m-%d %H:%M")
