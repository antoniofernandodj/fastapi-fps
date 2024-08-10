from fastapi import Depends
from typing import Annotated
from fps_src.core.security import (
    current_user
)
from fps_src.infra.database.user import User

current_user_dependency = Annotated[User, Depends(current_user)]
