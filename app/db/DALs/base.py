from abc import ABC, abstractmethod
from typing import Type, AsyncGenerator

from sqlalchemy import Column, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base

__all__ = ['BaseDAL']


class BaseDAL(ABC):
    """Abstract Data Access Layer class"""
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        pass

    @property
    @abstractmethod
    def pk(self) -> Column:
        pass

    async def flush(self):
        await self.session.flush()

    async def objects(self) -> AsyncGenerator[Base, None]:
        stream = await self.session.stream(select(self.model))
        async for instance in stream.scalars():
            yield instance

    async def create(self, **kw):
        instance = self.model(**kw)
        self.session.add(instance)
        return instance

    async def update(self, instance, **kw):
        for key in kw:
            if not hasattr(instance, key):
                raise AttributeError(f'Try to update not existing field `{key}` for type `{type(instance)}`')
            setattr(instance, key, kw[key])
        self.session.add(instance)

    async def delete(self, instance):
        await self.session.delete(instance)
