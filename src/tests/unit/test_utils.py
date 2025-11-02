from utils import get_version


def test_get_version() -> None:
    version = get_version()
    major, minor, patch = version.split(".")

    assert isinstance(version, str)
    assert major.isdigit()
    assert minor.isdigit()
    assert patch.isdigit()
