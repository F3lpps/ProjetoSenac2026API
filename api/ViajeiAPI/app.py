from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ViajeiAPI.database import get_session
from ViajeiAPI.models import User
from ViajeiAPI.schemas.message import Message
from ViajeiAPI.schemas.user import Userlist, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/")
def read_root():
    return {"message": "(⌐■_■)👌"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def register(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail="This username already exists"
            )
        elif db_user.email == user.email:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail="This email already exists"
            )

    db_user = User(username=user.username, email=user.email, senha=user.senha)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=Userlist)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
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


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.senha = user.senha
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user
