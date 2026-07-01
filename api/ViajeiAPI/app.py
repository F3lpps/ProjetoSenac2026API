from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from ViajeiAPI.schemas.message import Message
from ViajeiAPI.schemas.user import User, UserDB, Userlist, UserPublic

app = FastAPI()

database = []


@app.get("/")
def read_root():
    return {"message": "(⌐■_■)👌"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def register(user: User):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get("/users/", response_model=Userlist)
def read_users():
    return {"users": database}


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {"message": "User deleted!"}


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return database[user_id - 1]
