from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/')
async def root() -> str:
    return 'Главная страница'


@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_users(username: str = Path(min_length=3, max_length=30, description='Enter username'),
                       age: int = Path(ge=1, le=120, description='Enter age')) -> User:
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int, username: str = Path(min_length=3, max_length=30, description='Enter username'),
                       age: int = Path(ge=1, le=120, description='Enter age')) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delite_user(user_id: int) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail='User was not found')


# uvicorn module_16_4:app --reload
