from fastapi import FastAPI
from pydantic import BaseModel


class MyItem(BaseModel):
    name: str
    price: float = 120.3
    ready: int = 1


app = FastAPI()


@app.get("/")
async def say_hello():
    return "Hello, Hieu!"


@app.post("/submit")
async def submit(item: MyItem):
    print(item.name)
    return item.name
