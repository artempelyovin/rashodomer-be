import gettext
import uuid
from datetime import UTC, datetime

_ = gettext.gettext


class UnsetValue:
    __slots__ = ()

    def __new__(cls) -> "UnsetValue":
        try:
            return UNSET
        except NameError:
            return super().__new__(cls)

    def __repr__(self) -> str:
        return "<unset>"


UNSET = UnsetValue()


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)
