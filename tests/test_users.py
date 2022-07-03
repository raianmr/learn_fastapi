import app.schemas as sc
from app.config import settings as se
from fastapi import status
from jose import jwt
from pytest import mark

# remember to use trailing '/'


def test_create_user(client):
    resp = client.post("/users/", json={"email": "test2@test.com", "password": "test"})
    new_user = sc.UserRead(**resp.json())
    assert resp.status_code == status.HTTP_201_CREATED


def test_login(dummy_user, client):
    resp = client.post(
        "/login/",
        data={"username": dummy_user["email"], "password": dummy_user["password"]},
    )
    login_resp = sc.Token(**resp.json())

    payload = jwt.decode(
        login_resp.access_token, key=se.secret_key, algorithms=[se.hash_algo]
    )
    user_id: str | None = payload.get("user_id")
    assert user_id == dummy_user["id"]
    assert login_resp.token_type == "bearer"
    assert resp.status_code == status.HTTP_200_OK


@mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (None, "test", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("test@test.com", "wrongpass", status.HTTP_403_FORBIDDEN),
        ("wrongemail", "test", status.HTTP_403_FORBIDDEN),
        ("wrong@email.com", "wrongpass", status.HTTP_403_FORBIDDEN),
        ("wrongemail", "wrongpass", status.HTTP_403_FORBIDDEN),
    ],
)
def test_incorrect_login(dummy_user, client, email, password, status_code):
    resp = client.post(
        "/login/",
        data={"username": email, "password": password},
    )
    assert resp.status_code == status_code
