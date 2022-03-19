from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

__all__ = ('User', )


Base = declarative_base()


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
