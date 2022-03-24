from .base import BaseDAL
from ..models.user import User


__all__ = ['UserDAL']


class UserDAL(BaseDAL):
    model = User

