from fastapi import HTTPException
from starlette import status

IncorrectCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

UnavailableCredentialsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Credenciais não disponíveis'
)
