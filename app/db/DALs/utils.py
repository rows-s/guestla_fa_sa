from contextlib import asynccontextmanager
from typing import TypeVar, AsyncContextManager, Type

from ..sessions import async_session_maker

__all__ = ['dal_maker']
_T = TypeVar('_T')


@asynccontextmanager
async def dal_maker(class_: Type[_T]) -> AsyncContextManager[_T]:
    async with async_session_maker() as session:
        yield class_(session)
        await session.commit()
