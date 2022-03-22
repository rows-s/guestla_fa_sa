from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

__all__ = ('User', 'UserCreate')


Base = declarative_base()


class UserCreate(BaseModel):
    email: str
    password: str


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)
