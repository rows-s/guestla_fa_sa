from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import *

url = 'postgresql+asyncpg://testuser:TESTpassW0RD@localhost/test'


@asynccontextmanager
async def make_async_session(create_engine_kw=None) -> AsyncSession:
    try:
        engine = create_async_engine(url, **(create_engine_kw or {}))
        async_session = sessionmaker(engine, class_=AsyncSession)
        async with async_session() as session:
            yield session
    finally:
        pass

