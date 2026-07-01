from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    senha: str


class UserDB(User):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class Userlist(BaseModel):
    users: list[UserPublic]
