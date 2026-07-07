from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from ViajeiAPI.app import app
from ViajeiAPI.database import get_session
from ViajeiAPI.models import User, table_registry
from ViajeiAPI.security import get_current_user, get_passwordhash


@contextmanager
def _execute_mock_time(*, model, time=datetime(2026, 6, 17)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _execute_mock_time


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def user(session):
    senha = 'testtest'
    user = User(
        username="Teste",
        email="teste@test.com",
        senha=get_passwordhash('testtest'),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_senha = senha

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth',
        data={'username': user.email, 'password': user.clean_senha},
    )
    return response.json()['create_token']


@pytest.fixture
def authenticated_user(client, user):
    def mock_get_current_user():
        return user

    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield client

    app.dependency_overrides.clear()
