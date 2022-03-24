from abc import ABC, abstractmethod
from typing import Type, AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base

__all__ = ['BaseDAL']


class BaseDAL(ABC):
    """Abstract Data Access Layer class"""
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        pass

    async def flush(self):
        await self.session.flush()

    async def get(self, pk):
        print(self.model.pk)
        result = await self.session.execute(select(self.model).where(self.model.pk == pk))
        return result.scalar()

    async def objects(self) -> AsyncGenerator[Base, None]:
        stream = await self.session.stream(select(self.model))
        return stream.scalars()

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
