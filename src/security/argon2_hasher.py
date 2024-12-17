from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


class Argon2PasswordHasher:
    def __init__(self):
        self.password_hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def verify_password(self, hashed_password: str, plain_password: str) -> bool:
        try:
            return self.password_hasher.verify(hashed_password, plain_password)
        except (VerifyMismatchError, VerificationError):
            return False