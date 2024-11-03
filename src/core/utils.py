import gettext
import uuid

_ = gettext.gettext


def uuid4_str() -> str:
    return str(uuid.uuid4())
