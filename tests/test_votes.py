import app.schemas as sc
import app.models as mo
from app.config import settings as se
from fastapi import status
from jose import jwt
from pytest import fixture, mark


def test_cast_vote(authorized_client, dummy_posts):
    resp = authorized_client.post(
        "/votes/", json={"post_id": dummy_posts[-1].id, "is_upvote": False}
    )

    assert resp.status_code == status.HTTP_201_CREATED


def test_cast_vote_twice(authorized_client, dummy_vote, dummy_posts):
    resp = authorized_client.post(
        "/votes/", json={"post_id": dummy_posts[0].id, "is_upvote": False}
    )

    assert resp.status_code == status.HTTP_409_CONFLICT

def test_cast_vote_on_nonexistent_post(authorized_client, dummy_posts):
    resp = authorized_client.post(
        "/votes/", json={"post_id": 420, "is_upvote": False}
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
