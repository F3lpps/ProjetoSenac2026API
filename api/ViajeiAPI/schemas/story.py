from ViajeiAPI_schemas.user import User


class Story:
    name: str
    title: str
    email = User.email
    body: str
