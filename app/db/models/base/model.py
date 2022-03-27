from sqlalchemy import inspect, Column, Integer
from sqlalchemy.orm import declarative_base


__all__ = ['Base']


sa_Base = declarative_base()


class Base(sa_Base):
    """Abstract base class for models"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    def dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    @classmethod
    @property
    def pk(cls):
        return inspect(cls).primary_key[0]
