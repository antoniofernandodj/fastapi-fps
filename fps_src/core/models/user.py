from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    __tablename__ = "user_account"
    username: str
    email: str
    fullname: str
    password_hash: Optional[str] = None
    id: Optional[str] = None
