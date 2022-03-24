from contextlib import asynccontextmanager
from typing import TypeVar, ContextManager, AsyncGenerator

from ..DALs import *
from ..sessions import async_session_maker

__all__ = ['dal_maker', 'get_user_dal']
_T = TypeVar('_T')


@asynccontextmanager
async def dal_maker(class_: _T) -> ContextManager[_T]:
    async with async_session_maker() as session:
        yield class_(session)
        await session.commit()


async def get_user_dal() -> AsyncGenerator[UserDAL, None]:
    async with dal_maker(UserDAL) as dal:
        yield dal
