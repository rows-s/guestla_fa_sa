import pydantic
from sqlalchemy import Column, Integer, String

from .base import Base

__all__ = ['User', 'UserCreate']


class UserCreate(pydantic.BaseModel):
    email: str
    password: str


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
