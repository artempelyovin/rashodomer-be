import uuid
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def uuid4_str() -> str:
    return str(uuid.uuid4())
