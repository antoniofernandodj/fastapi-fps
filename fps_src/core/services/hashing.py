import base64
import bcrypt
from typing import Any


class HashService:

    @classmethod
    def hash(cls, password: str):
        salt = bcrypt.gensalt()
        hashpw = bcrypt.hashpw(password.encode("utf-8"), salt)
        hash_base64 = base64.b64encode(hashpw).decode("utf-8")
        return hash_base64

    @classmethod
    def check(cls, password_hash: Any, senha_usuario: str) -> bool:
        hash_bytes = base64.b64decode(password_hash.encode("utf-8"))
        return bcrypt.checkpw(senha_usuario.encode("utf-8"), hash_bytes)
