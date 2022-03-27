from contextlib import asynccontextmanager
from typing import TypeVar, AsyncContextManager, Type

from .base import BaseDAL
from ..sessions import async_session_maker

__all__ = ['dal_maker']
_DAL = TypeVar('_DAL', bound=BaseDAL)


@asynccontextmanager
async def dal_maker(class_: Type[_DAL]) -> AsyncContextManager[_DAL]:
    async with async_session_maker() as session:
        dal = class_(session)
        yield dal
        await dal.commit()
