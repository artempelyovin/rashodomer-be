import gettext
import tomllib
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator

_ = gettext.gettext


def get_version() -> str:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with Path.open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    return str(data["project"]["version"])


def uuid4_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def validate_uuid4(value: str) -> str:
    uuid.UUID(value, version=4)
    return value


UUID4Str = Annotated[str, AfterValidator(validate_uuid4)]
