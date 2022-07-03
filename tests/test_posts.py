import app.schemas as sc
from app.config import settings as se
from fastapi import status
from jose import jwt
from pytest import mark

# remember to use trailing '/'


def test_get_all_posts(authorized_client, dummy_posts):
    resp = authorized_client.get("/posts/")

    assert len(resp.json()) == len(dummy_posts)
    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_get_all_posts(client, dummy_posts):
    resp = client.get("/posts/")

    assert len(resp.json()) != len(dummy_posts)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post(authorized_client, dummy_posts):
    resp = authorized_client.get(f"/posts/{dummy_posts[-1].id}")

    assert resp.status_code == status.HTTP_200_OK


def test_unauthorized_get_one_post(client, dummy_posts):
    resp = client.get(f"/posts/{dummy_posts[-1].id}")

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_nonexistent_post(authorized_client):
    resp = authorized_client.get(f"/posts/420")

    assert resp.status_code == status.HTTP_404_NOT_FOUND


@mark.parametrize(
    "title, content, published",
    [
        ("generic title", "generic content", True),
        ("generic title", "generic content", False),
        (69, 420, False),
    ],
)
def test_create_post(authorized_client, title, content, published):
    post_data = {"title": title, "content": content, "published": published}
    resp = authorized_client.post("/posts/", json=post_data)

    assert resp.status_code == status.HTTP_201_CREATED


def test_unauthorized_create_post(client):
    post_data = {"title": "pero", "content": "pero", "published": "pero"}
    resp = client.post("/posts/", json=post_data)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(authorized_client, dummy_post):
    resp = authorized_client.delete(f"/posts/{dummy_post['id']}")

    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_unauthorized_delete_post(client):
    resp = client.delete(f"/posts/420")

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_nonexistent_post(authorized_client):
    resp = authorized_client.delete(f"/posts/420")

    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_users_post(authorized_client, dummy_posts):
    resp = authorized_client.delete(f"/posts/{dummy_posts[-1].id}")

    assert resp.status_code == status.HTTP_403_FORBIDDEN
