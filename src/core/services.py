from abc import ABC, abstractmethod

type Total = int


class PasswordService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def check_password(self, password: str, password_hash: str) -> bool: ...


class EmojiService(ABC):
    @abstractmethod
    def is_emoji(self, emoji_text: str) -> bool: ...


class TokenService(ABC):
    @abstractmethod
    async def create_new_token(self, user_id: str) -> str: ...

    @abstractmethod
    async def get_user_id_by_token(self, token: str) -> str | None: ...
