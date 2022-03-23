from sqlalchemy.ext.asyncio import AsyncSession as sa_AsyncSession
from sqlalchemy.orm import sessionmaker

from .engines import base_engine

__all__ = ['AsyncSession', 'async_session_maker']


async_session_maker = sessionmaker(base_engine, expire_on_commit=False, class_=sa_AsyncSession)


class AsyncSession:
    """
    Async context manager / Session container. Use only in `async with` statement.

    Warnings:
        expire_on_commit=False by default. The session is closed on exit the context manager.

    Examples:
        >>> async with AsyncSession() as session:
        >>>     pass

        >>> session_container = AsyncSession()  # don't name it `session`, may confuse. `container`, `maker` whatever
        >>> async with session_container as session:
        >>>     pass
    """
    def __init__(self, session_maker: sessionmaker = async_session_maker):
        self.session: sa_AsyncSession = session_maker()

    async def __aenter__(self) -> sa_AsyncSession:
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        # close
        await self.session.close()


