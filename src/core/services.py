from typing import Protocol


class PasswordService(Protocol):
    def hash_password(self, password: str) -> str: ...
