import uuid
from datetime import UTC, datetime
from typing import Final


def utc_now() -> datetime:
    return datetime.now(UTC)


def uuid4_str() -> str:
    return str(uuid.uuid4())


class Unset:
    """Sentinel for distinguishing 'not provided' from None in optional updates."""

    def __repr__(self) -> str:
        return "UNSET"


UNSET: Final[Unset] = Unset()
