from sqlalchemy.ext.asyncio import AsyncSession as sa_AsyncSession
from sqlalchemy.orm import sessionmaker

from .engines import base_engine

__all__ = ['AsyncSession']


class AsyncSession:
    """
    Async context manager / Session container. Use only in `async with` statement.

    Examples:
        >>> async with AsyncSession() as session:
        >>>     pass

        >>> session_container = AsyncSession()  # don't name it `session`, may confuse: `container`, `maker` whatever
        >>> async with session_container as session:
        >>>     pass
    """
    def __init__(self, engine=base_engine, **kw):
        self.session: sa_AsyncSession = sessionmaker(engine, class_=sa_AsyncSession, **kw)()

    async def __aenter__(self) -> sa_AsyncSession:
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        await self.session.close()


