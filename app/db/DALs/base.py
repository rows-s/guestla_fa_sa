from abc import ABC, abstractmethod
from typing import Type, AsyncGenerator, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncScalarResult

from ..models.base import Base
from ..utils import dal_maker

__all__ = ['BaseDAL']

_T = TypeVar('_T')


class BaseDAL(ABC):
    """Abstract Data Access Layer class"""
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        pass

    @classmethod
    async def generate_dal(cls: Type[_T]) -> AsyncGenerator[_T, None]:
        """
        Only once yields DAL matching to `cls`.
        Best case is to use within `FastAPI.Depends`.
        In custom usage must be called second time to make session closed and committed.
        """
        async with dal_maker(cls) as dal:
            yield dal

    async def get(self, pk):
        print(self.model.pk)
        result = await self.session.execute(select(self.model).where(self.model.pk == pk))
        return result.scalar()

    async def objects(self) -> AsyncScalarResult:
        stream = await self.session.stream(select(self.model))
        return stream.scalars()

    async def create(self, *, shld_flush=False, **kw):
        instance = self.model(**kw)
        self.session.add(instance)
        if shld_flush:
            await self.flush()
        return instance

    async def update(self, instance, shld_flush=False, **kw):
        for key in kw:
            if not hasattr(instance, key):
                raise AttributeError(f'Try to update not existing field `{key}` for type `{type(instance)}`')
            setattr(instance, key, kw[key])
        self.session.add(instance)
        if shld_flush:
            await self.flush()

    async def delete(self, instance):
        await self.session.delete(instance)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()
