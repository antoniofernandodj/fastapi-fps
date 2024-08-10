from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from fps_src.config import settings


class DatabaseConnectionManager:

    @classmethod
    def create_database(cls):
        engine = cls.get_engine()
        from fps_src.infra.database import Base
        Base.metadata.create_all(engine)

    @classmethod
    def get_async_engine(cls):
        return create_async_engine(
            settings.DATABASE_ASYNC_URL,
            future=True,
            echo=True
        )
    
    @classmethod
    def get_engine(cls):
        return create_engine(
            settings.DATABASE_SYNC_URL,
            future=True,
            echo=True
        )


AsyncSessionFactory = sessionmaker(
    DatabaseConnectionManager.get_async_engine(),  # type: ignore
    expire_on_commit=False,
    class_=AsyncSession
)