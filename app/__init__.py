from fastapi import FastAPI

from . import db
from . import fix_issue_837

app = FastAPI()


@app.get('/')
async def root():
    return {"you've made root request": True}


@app.get('/user/{user_id}')
async def read_user(user_id: str):
    return {'user u wanna get': user_id}


@app.post('/user')
async def post_user(user: db.UserCreate):
    async with db.make_async_session(expire_on_commit=False) as session:
        user = db.User(email=user.email, password=user.password)
        session.add(user)
    print(f"Added user {user.id}")
    return {'id': user.id}
