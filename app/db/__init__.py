from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import *

url = 'postgresql+asyncpg://testuser:TESTpassW0RD@localhost/test'  # TODO: use env var
engine = create_async_engine(url)


@asynccontextmanager
async def make_async_session(engine_=engine, **kw) -> AsyncSession:
    session = sessionmaker(engine_, class_=AsyncSession, **kw)()  # called!
    try:
        yield session
        # else block:
        await session.commit()
    finally:
        await session.close()

