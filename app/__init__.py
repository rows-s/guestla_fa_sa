from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.future import select

from . import db

app = FastAPI()


@app.get('/')
async def root():
    return {"you've made root request": True}


@app.get('/user/{user_id}')
async def read_user(user_id: int):
    async with db.AsyncSession(expire_on_commit=False) as session:
        users = await session.execute(select(db.User).where(db.User.id == user_id))
        user = users.scalar()
        if user is None:
            raise HTTPException(404, f'User with `id={user_id}` not found')
    return user._asdict()


@app.post('/user')
async def post_user(user: db.UserCreate):
    async with db.AsyncSession(expire_on_commit=False) as session:
        user = db.User(**user.dict())
        session.add(user)
    print(f"Added user {user.id}")
    return {'id': user.id}
