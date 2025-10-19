import gettext
import uuid
from datetime import UTC, datetime

_ = gettext.gettext


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)
