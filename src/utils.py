import gettext
import uuid
from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator

_ = gettext.gettext


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def validate_uuid4(value: str) -> str:
    uuid.UUID(value, version=4)
    return value


UUID4Str = Annotated[str, AfterValidator(validate_uuid4)]
