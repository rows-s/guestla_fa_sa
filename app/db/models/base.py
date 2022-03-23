from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base


__all__ = ['Base']

sa_Base = declarative_base()


class Base(sa_Base):
    __abstract__ = True

    def asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
