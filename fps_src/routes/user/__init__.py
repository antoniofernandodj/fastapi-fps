from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from fps_src.exceptions import (
    IncorrectCredentialsException, UnavailableCredentialsException
)

from fps_src.core.services import UserService
from fps_src.core.models import UserRequest, Token
from fps_src.core.security import authenticate_user, create_access_token
from fps_src.core.dependecies import current_user_dependency

router = APIRouter()


@router.post('/user')
async def cadastrar(
    user: UserRequest,
    user_service: UserService = Depends(UserService)
):
    id = await user_service.cadastrar_usuario(user)
    if id == 0:
        raise UnavailableCredentialsException

    return {'id': id}


@router.post("/login", response_model=Token)
async def login_post(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:

    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise IncorrectCredentialsException

    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
    }


@router.get("/protected")
async def home(current_user: current_user_dependency):
    return {'user': current_user.username}
