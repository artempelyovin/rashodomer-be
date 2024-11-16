import bcrypt
import emoji

from core.services import EmojiService, PasswordService


class PasswordBcryptService(PasswordService):
    def hash_password(self, password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_.decode()

    def check_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())


class EmojiPackageService(EmojiService):
    def is_emoji(self, emoji_text: str) -> bool:
        return emoji.is_emoji(emoji_text)
