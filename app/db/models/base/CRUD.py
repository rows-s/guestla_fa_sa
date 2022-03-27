from abc import ABC

import pydantic

from ..utils import optional_fields

__all__ = ['BaseCreate', 'BasePatch', 'BaseRead']


class BaseCreate(pydantic.BaseModel, ABC):
    pass


@optional_fields(all_fields=True)
class BasePatch(BaseCreate, ABC):
    pass


class BaseRead(BaseCreate, ABC):
    id: str
