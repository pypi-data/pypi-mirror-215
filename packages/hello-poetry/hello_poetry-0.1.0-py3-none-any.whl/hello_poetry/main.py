from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str | None = None


app = FastAPI()


@app.get("/")
async def hello():
    return {"msg": "Hello, Poetry!"}


@app.get("/user/{username}")
async def get_user(username: str):
    return {"msg": "Hello, " + username}


@app.post("/user")
async def create_user(user: User):
    return {"msg": user.name.upper()}
