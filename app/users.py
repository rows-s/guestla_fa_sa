from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from . import db
from .tags import Tags

__all__ = ['router', 'tags']

router = APIRouter()
tags = [Tags.users]


@router.get('/')
async def iter_users(limit: int = 100):
    async with db.AsyncSession() as session:
        async for user in db.ModelDAL(session, db.User).objects():
            print(user.asdict())


@router.get('/{user_id}')
async def read_user(user_id: int):
    async with db.AsyncSession() as session:
        result = await session.execute(
            select(db.User).where(db.User.id == user_id)
        )
        user = result.scalar()
        if user is None:
            raise HTTPException(404, f'User with `id={user_id}` not found')
        return user.asdict()


@router.post('/')
async def post_user(user: db.UserCreate):
    async with db.AsyncSession() as session:
        user = db.User(**user.dict())
        session.add(user)
    print(f"Added user {user.id}")
    return {'id': user.id}
