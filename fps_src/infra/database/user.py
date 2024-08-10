from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    fullname: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(Text)
