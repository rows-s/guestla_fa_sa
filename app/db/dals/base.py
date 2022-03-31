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

    async def add_to_session(self, instance, shld_flush=False):
        self.session.add(instance)
        if shld_flush:
            await self.flush()

    async def get(self, pk):
        return await self.session.get(self.model, pk)

    async def objects(self) -> AsyncScalarResult:
        return await self.session.stream_scalars(select(self.model))

    async def create(self, *, shld_flush=False, **kw):
        instance = self.model(**kw)
        await self.add_to_session(instance, shld_flush=shld_flush)
        return instance

    async def update(self, instance, shld_flush=False, **kw):
        for key in kw:
            if not hasattr(instance, key):
                raise AttributeError(f'Try to update not existing field `{key}` for type `{type(instance)}`')
            setattr(instance, key, kw[key])
        await self.add_to_session(instance, shld_flush=shld_flush)

    async def delete(self, instance):
        await self.session.delete(instance)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()
