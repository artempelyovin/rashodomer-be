import bcrypt

from core.services import PasswordService


class PasswordBcryptService(PasswordService):
    def hash_password(self, password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_.decode()

    def check_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
