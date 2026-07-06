from http import HTTPStatus

from jwt import decode

from ViajeiAPI.security import SECRET_KEY, create_token


def test_jwt():

    # GIVEN; DADO
    data = {"test": "test"}
    token = create_token(data)

    # WHEN; QUANDO
    decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
