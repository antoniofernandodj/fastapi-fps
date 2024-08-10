from fps_src.core.repositories.base import Repository


class UserRepository(Repository):
    from fps_src.infra.database import User

    model_class = User
