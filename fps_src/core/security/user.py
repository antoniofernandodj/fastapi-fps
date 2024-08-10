from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fps_src.config import settings as s
from fps_src.core.repositories import UserRepository
from fps_src.core.services.hashing import HashService
from fps_src.core.models import TokenData
from .scheme import oauth2_scheme
from fps_src.infra.database.config import AsyncSessionFactory
from fps_src.infra.database.user import User


async def authenticate_user(
    username: str, password: str
) -> Optional[User]:

    async with AsyncSessionFactory() as session:  # type: ignore
        user_repo = UserRepository(session)

        user = await user_repo.find_one(username=username)
        if user is None or not isinstance(user, User):
            return None

        if not HashService.check(user.password_hash, password):
            return None

        return user


async def current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, s.SECRET_KEY, algorithms=[s.AUTH_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    async with AsyncSessionFactory() as session:  # type: ignore
        user_repo = UserRepository(session)

        user = await user_repo.find_one(username=token_data.username)

        if user is None or not isinstance(user, User):
            raise credentials_exception

        return user
