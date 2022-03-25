from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import IntegrityError

from app import db
from app.db.utils import get_user_dal
from app.sub_apps.config import Tags

__all__ = ['router', 'tags']

router = APIRouter()
tags = [Tags.users]


@router.get('')
async def read_users(
        page_size: int = Query(100, le=100),
        user_dal: db.UserDAL = Depends(get_user_dal)
):
    users_gen = await user_dal.objects()
    async for page in users_gen.partitions(page_size):
        return {'data': {'users': page}}


@router.get('/{user_id}')
async def read_user(
        user_id: int,
        user_dal: db.UserDAL = Depends(get_user_dal)
):
    user = await user_dal.get(user_id)
    if user is None:
        raise HTTPException(404, f"user with `id={user_id}` doesn't exist")
    return {'data': {'user': user.asdict()}}


@router.post('')
async def post_user(
        user: db.UserCreate,
        user_dal: db.UserDAL = Depends(get_user_dal)
):
    try:
        user = await user_dal.create(**user.dict(), shld_flush=True)
    except IntegrityError:  # TODO: Must check which column is duplicated
        raise HTTPException(409, f'user with `email={user.email}` already exist')
    else:
        return {'data': {'id': user.id}}
