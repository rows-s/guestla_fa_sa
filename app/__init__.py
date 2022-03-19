from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def root():
    return {"you've made root request": True}


@app.get('/user/{user_id}')
async def get_user(user_id: str):
    return {'user u wanna get': user_id}
