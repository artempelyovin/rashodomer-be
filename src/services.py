import bcrypt


class PasswordBcryptService:
    @staticmethod
    def hash_password(password: str) -> str:
        hash_ = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_.decode()

    @staticmethod
    def check_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
