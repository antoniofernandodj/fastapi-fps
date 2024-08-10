from typing import List, Optional, Any
from asyncio import Lock
from sqlalchemy import update, insert, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


class Repository:
    """A generic repository class to interact with a database table
    for a Pydantic model."""

    model_class: type

    def __init__(self, session: Session):
        self.session = session
        self.lock = Lock()

    async def find_one(self, **kwargs) -> Optional[Any]:
        cls = type(self)
        try:
            stmt = select(cls.model_class).filter_by(**kwargs)  # type: ignore

            result = await self.session.execute(stmt)  # type: ignore
            return result.scalars().one()

        except NoResultFound:
            return None

    async def find_all(self, **kwargs) -> List[Any]:
        query = select(self.model_class).filter_by(**kwargs)  # type: ignore
        result = await self.session.execute(query)  # type: ignore
        return result.scalars().all()

    async def save(self, entity: Any) -> bool:
        cls = type(self)
        data = entity.model_dump()  # entity is a pydantic base model
        print(data)
        try:
            sql = insert(cls.model_class).values(**data)
            sql.execution_options(synchronize_session='fetch')
            async with self.lock:
                await self.session.execute(sql)  # type: ignore
                await self.session.commit()  # type: ignore

        except Exception as erro:
            print({'erro': erro})
            return False
        return True

    async def update(self, item: Any, data: dict = {}) -> int:
        try:
            sql = (
                update(self.model_class)
                .where(self.model_class.id == item.id)  # type: ignore
                .values(**data)
            )
            sql.execution_options(synchronize_session='fetch')
            async with self.lock:
                result = await self.session.execute(sql)  # type: ignore
                await self.session.commit()  # type: ignore
            return result.rowcount
        except Exception as error:
            print({'error': error})
            return 0

    async def delete(self, item: Any) -> int:
        try:
            sql = (
                delete(self.model_class)
                .where(self.model_class.id == item.id)  # type: ignore
            )
            async with self.lock:
                result = await self.session.execute(sql)  # type: ignore
                await self.session.commit()  # type: ignore
            return result.rowcount
        except Exception as error:
            print({'error': error})
            return 0

    async def delete_from_id(self, id) -> int:
        try:
            sql = (
                delete(self.model_class)
                .where(self.model_class.id == id)  # type: ignore
            )
            async with self.lock:
                result = await self.session.execute(sql)  # type: ignore
                await self.session.commit()  # type: ignore
            return result.rowcount
        except Exception as error:
            print({'error': error})
            return 0
