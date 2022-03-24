from fastapi import APIRouter, HTTPException, Depends

from . import db
from .db.utils import get_user_dal
from .tags import Tags

__all__ = ['router', 'tags']

router = APIRouter()
tags = [Tags.users]


@router.get('/')
async def iter_users(user_dal=Depends(get_user_dal)):
    users_gen = user_dal.objects()
    return {'users': await users_gen.all()}


@router.get('/{user_id}')
async def read_user(
        user_id: int,
        user_dal=Depends(get_user_dal)
):
    user = await user_dal.get(user_id)
    if user is None:
        raise HTTPException(404, f"user with `id={user_id}` doesn't exist")
    return user.asdict()


@router.post('/')
async def post_user(
        user: db.UserCreate,
        user_dal: db.UserDAL = Depends(get_user_dal)
):
    user = await user_dal.create(**user.dict())
    await user_dal.flush()
    return {'id': user.id}
