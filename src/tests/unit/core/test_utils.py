from uuid import UUID

from core.utils import uuid4_str


def test_uuid4_str() -> None:
    uuid4_as_str = uuid4_str()
    UUID(uuid4_as_str)
