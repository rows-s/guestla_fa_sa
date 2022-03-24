from fastapi import APIRouter, HTTPException

from . import db
from .db.utils import user_dal_maker
from .tags import Tags

__all__ = ['router', 'tags']

router = APIRouter()
tags = [Tags.users]


@router.get('/')
async def iter_users():
    async with user_dal_maker() as user_dal:
        return {'users': await (await user_dal.objects()).all()}


@router.get('/{user_id}')
async def read_user(user_id: int):
    async with user_dal_maker() as user_dal:
        user = await user_dal.get(user_id)
        if user is None:
            raise HTTPException(404, f"user with `id={user_id}` doesn't exist")
        return user.asdict()


@router.post('/')
async def post_user(user: db.UserCreate):
    async with user_dal_maker() as user_dal:
        user = await user_dal.create(**user.dict())
    print(f"Added user {user.id}")
    return {'id': user.id}
