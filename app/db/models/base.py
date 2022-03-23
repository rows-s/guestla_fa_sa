from abc import ABC
from typing import AsyncGenerator

from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

__all__ = ['Base', 'ModelDAL']

sa_Base = declarative_base()


class Base(sa_Base):
    __abstract__ = True

    def asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class ModelDAL(ABC):
    def __init__(self, session: AsyncSession, model: Base):
        self.session: AsyncSession = session
        self.model: Base = model

    async def objects(self) -> AsyncGenerator[Base, None]:
        result = await self.session.stream(select(self.model))
        async for obj in result.scalars():
            yield obj



