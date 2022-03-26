from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import IntegrityError

from ... import db

__all__ = ['router']

router = APIRouter()


@router.get('')
async def read_users(
        page_size: int = Query(100, le=100),
        user_dal: db.UserDAL = Depends(db.UserDAL.generate_dal)
):
    users_gen = await user_dal.objects()
    async for page in users_gen.partitions(page_size):
        return {'data': {'users': page}}
    return {'data': {'users': []}}


@router.get('/{user_id}')
async def read_user(
        user_id: int,
        user_dal: db.UserDAL = Depends(db.UserDAL.generate_dal)
):
    user = await user_dal.get(user_id)
    if user is None:
        raise HTTPException(404, f"user with `id={user_id}` doesn't exist")
    return {'data': {'user': user.asdict()}}


@router.post('')
async def post_user(
        user: db.UserIn,
        user_dal: db.UserDAL = Depends(db.UserDAL.generate_dal)
):
    try:
        user = await user_dal.create(**user.dict(), shld_flush=True)
    except IntegrityError:  # TODO: Must check which column is duplicated
        raise HTTPException(409, f'user with `email={user.email}` already exist')
    else:
        return {'data': {'user': user}}


@router.put('')
async def post_user(
        user_dal: db.UserDAL = Depends(db.UserDAL.generate_dal)
):
    try:
        user = await user_dal.create(**user.dict(), shld_flush=True)
    except IntegrityError:  # TODO: Must check which column is duplicated
        raise HTTPException(409, f'user with `email={user.email}` already exist')
    else:
        return {'data': {'user': user}}
