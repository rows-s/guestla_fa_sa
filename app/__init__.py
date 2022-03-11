from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def root(required_query_arg: int):
    return {"you're in root": True}
