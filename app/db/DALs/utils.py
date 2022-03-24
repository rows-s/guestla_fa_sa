from contextlib import asynccontextmanager
from typing import TypeVar, ContextManager

from ..DALs import *
from ..sessions import async_session_maker

__all__ = ['dal_maker', 'user_dal_maker']
_T = TypeVar('_T')


@asynccontextmanager
async def dal_maker(class_: _T) -> ContextManager[_T]:
    async with async_session_maker() as session:
        yield class_(session)


@asynccontextmanager
async def user_dal_maker() -> ContextManager[UserDAL]:
    async with dal_maker(UserDAL) as dal:
        yield dal
