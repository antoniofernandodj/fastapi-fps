from fps_src.core.repositories import UserRepository
from fps_src.infra.database.config import AsyncSessionFactory
from fps_src.core.models import UserRequest, User

import uuid


class UserService:

    def __init__(self):
        self.factory = AsyncSessionFactory 
        self.repo = UserRepository

    async def cadastrar_usuario(self, user_request: UserRequest):
        from fps_src.core.services import HashService

        if user_request.password is None:
            raise AttributeError('Usuario sem senha!')

        id = str(uuid.uuid4())
        async with self.factory() as session:  # type: ignore
            user_repo = self.repo(session)
            user_data = user_request.model_dump()

            query1 = await user_repo.find_one(username=user_data['username'])
            query2 = await user_repo.find_one(email=user_data['email'])
            q = query1 or query2
            print({'q': q})
            if q:
                return 0

            user_data['password_hash'] = HashService.hash(
                user_request.password
            )
            del user_data['password']

            user = User(**user_data)
            user.id = id
            success = await user_repo.save(user)
            if success:
                return id

        raise Exception
