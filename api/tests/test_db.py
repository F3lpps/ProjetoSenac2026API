from dataclasses import asdict

from sqlalchemy import select

from ViajeiAPI.models import User


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
