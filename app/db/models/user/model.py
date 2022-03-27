from sqlalchemy import Column, String

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
