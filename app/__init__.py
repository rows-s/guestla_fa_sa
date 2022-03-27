from fastapi import FastAPI

from .sub_apps import users

__all__ = ['app']


app = FastAPI()
app.include_router(users.router, prefix='/users', tags=users.tags)
