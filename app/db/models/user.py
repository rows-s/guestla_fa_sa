import pydantic
from sqlalchemy import Column, Integer, String

from . import base

__all__ = ['User', 'UserCreate']


class User(base.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class UserCreate(pydantic.BaseModel):
    email: str
    password: str
