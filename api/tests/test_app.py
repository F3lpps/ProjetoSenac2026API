from http import HTTPStatus


def read_root():
    return {"message": "(⌐■_■)👌"}


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "username": "baianinhodemaua",
            "email": "baianinho@example.com",
            "senha": "secret",
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "baianinhodemaua",
        "email": "baianinho@example.com",
        "id": 1,
    }


def test_delete_user(client):

    # When
    response = client.delete("/users/1")

    # Then
    response.status_code == HTTPStatus.OK
    response.json() == {"message": "User deleted!"}


def test_delete_404(client):

    response = client.delete("/users/0")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"message": "User not found"}


def test_get_200(client):

    response = client.get("/users/1")

    response.status_code == HTTPStatus.OK
    response.json() == {
        "email": "baianinho@example.com",
        "id": 1,
    }


def test_get_notfound(client):

    response = client.get("/users/0")

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {"detail": "User not found"}


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "baianinhodemaua",
                "email": "baianinho@example.com",
                "id": 1,
            }
        ]
    }
