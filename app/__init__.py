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
    user = db.User(email=user.email, password=user.password)
    async with db.make_async_session() as session:
        async with session:
            session.add_all([user])

    return {'id': user.id}
