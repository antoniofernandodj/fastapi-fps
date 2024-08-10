from fps_src.infra.database.config import (
    AsyncSessionFactory, DatabaseConnectionManager
)
from fps_src.core.repositories import UserRepository
from fps_src.core.models import UserRequest, User
from fps_src.core.services import UserService


async def test_async_session_factory():
    async with AsyncSessionFactory() as session:  # type: ignore
        assert session


async def test_create_database():
    DatabaseConnectionManager.create_database()
    assert True


async def test_user_repository():

    async with AsyncSessionFactory() as session:  # type: ignore
        user_repo = UserRepository(session)
        user = User(
            id='id',
            username='username',
            email='email',
            fullname='fullname',
            password_hash='password_hash'
        )
        result = await user_repo.save(user)
        print(result)

    assert True


async def test_user_service():
    us = UserService()

    user = UserRequest(
        username='username2',
        email='email2',
        fullname='fullname',
        password='password'
    )
    id = await us.cadastrar_usuario(user)

    assert isinstance(id, str)
