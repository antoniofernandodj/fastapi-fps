from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    __tablename__ = "user_account"
    username: str
    email: str
    fullname: str
    password: str
