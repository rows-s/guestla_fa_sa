from sqlalchemy.ext.asyncio import create_async_engine

from .config import DSN

__all__ = ['base_engine']


base_engine = create_async_engine(DSN)
