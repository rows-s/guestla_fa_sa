from fastapi import FastAPI

from . import db
from . import users

app = FastAPI()
app.include_router(users.router, prefix='/users', tags=users.tags)
