from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from ViajeiAPI.models import Story, User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="baianinhodemaua",
            senha="secret",
            email="baianinho@example.com",
        )

        session.add(new_user)
        session.commit()

    user = session.scalar(
        select(User).where(User.username == "baianinhodemaua")
    )

    assert asdict(user) == {
        "id": 1,
        "username": "baianinhodemaua",
        "senha": "secret",
        "email": "baianinho@example.com",
        "created_at": time,
    }


def test_create_story(session, mock_db_time, user):
    with mock_db_time(model=Story):
        new_story = Story(author="jj", title="Titulo", story="Era uma vez...")
        new_story.email = user.email

    session.add(new_story)
    session.commit()

    story = session.scalar(select(Story).where(Story.author == "jj"))

    # Transforma em dicionário
    story_dict = asdict(story)

    created_at_value = story_dict.pop("created_at")

    assert story_dict == {
        "id": 1,
        "author": "jj",
        "title": "Titulo",
        "email": user.email,
        "story": "Era uma vez...",
    }

    assert isinstance(created_at_value, datetime)
