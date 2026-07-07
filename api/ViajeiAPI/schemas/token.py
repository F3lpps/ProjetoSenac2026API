from pydantic import BaseModel


class Token(BaseModel):
    create_token: str
    token_type: str


class StoryPublic(BaseModel):
    id: int
    title: str
    email: str
