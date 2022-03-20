from aiopg.sa.connection import SAConnection, Transaction
from aiopg.sa.engine import create_engine
from fastapi import FastAPI

from . import db
from . import fix_issue_837


app = FastAPI()


@app.get('/')
async def root():
    return {"you've made root request": True}


@app.get('/user/{user_id}')
async def get_user(user_id: str):
    return {'user u wanna get': user_id}
