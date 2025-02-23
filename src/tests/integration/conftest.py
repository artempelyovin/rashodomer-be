from collections.abc import Generator
from pathlib import Path

import pytest

from repos.files import JsonFileMixin


@pytest.fixture(autouse=True)
def remove_temp_file() -> Generator[None, None, None]:
    """Run after each test and deletes the temporary database file"""
    yield  # run test
    Path(JsonFileMixin.filename).unlink()  # remove teardown
