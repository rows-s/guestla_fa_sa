from ..base import BaseCreate, BasePatch, BaseRead
from ..utils import optional_fields

__all__ = ['UserCreate', 'UserPatch', 'UserRead']


class UserCreate(BaseCreate):
    email: str
    password: str


@optional_fields(all_fields=True)
class UserPatch(UserCreate, BasePatch):
    pass


class UserRead(UserCreate, BaseRead):
    pass
