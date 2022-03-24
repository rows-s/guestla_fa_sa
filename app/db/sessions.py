from sqlalchemy.ext.asyncio import AsyncSession as sa_AsyncSession
from sqlalchemy.orm import sessionmaker

from .engines import base_engine

__all__ = ['async_session_maker']


async_session_maker = sessionmaker(base_engine, expire_on_commit=False, class_=sa_AsyncSession)
