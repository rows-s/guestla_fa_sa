from typing import Iterable, Optional, Type, TypeVar

import pydantic

__all__ = ['optional_fields']


_fields_set = Optional[Iterable]
_T = TypeVar('_T', bound=pydantic.BaseModel)


def optional_fields(include: _fields_set = None, exclude: _fields_set = None, *, all_fields=False):
    """
    Class decorator. Makes `cls`' fields optional according to provided `all_fields`, `include` or `exclude`.

    Only one must be provided. If more than one provided uses first in given sequence.

    If nothing given `all_fields` is used.

    Examples:
         >>> class UserCreate(pydantic.BaseModel):
         ...    email: str

         >>> @optional_fields(all_fields=True)
         ... class UserPatch(UserCreate):
         ...    pass

         >>> UserPatch()
         UserPatch(email=None)
         >>> UserPatch.__fields__['email'].required
         False
    """
    def cls_decorator(cls: Type[_T]) -> Type[_T]:
        fields = set(cls.__fields__)

        if all_fields:  # no list
            pass
        elif include is not None:  # white list
            fields = set(include)
        elif exclude is not None:  # black list
            fields.difference_update(exclude)

        for field in fields:
            cls.__fields__[field].required = False
        return cls

    return cls_decorator
