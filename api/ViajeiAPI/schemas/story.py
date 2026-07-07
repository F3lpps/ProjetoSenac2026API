from pydantic import BaseModel


class StorySchema(BaseModel):
    author: str
    title: str
    story: str


class StoryPublic(BaseModel):
    id: int
    title: str
    email: str


class StoryDB(StorySchema):
    id: int
