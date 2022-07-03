import app.models as mo
import app.oauth2 as o2
from app.config import settings as se
from app.database import Base, get_db
from app.main import app
from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = f"{se.db_type}://{se.db_user}:{se.db_pass}@{se.db_host}:{se.db_port}/{se.db_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@fixture
def dummy_user(client):
    user_data = {"email": "test@test.com", "password": "test"}
    resp = client.post("/users/", json=user_data)

    new_user = resp.json()
    new_user["password"] = user_data["password"]

    return new_user


@fixture
def dummy_post(dummy_user, client):
    post_data = {
        "title": f"dummy post",
        "content": "initial content",
        "published": True,
    }
    resp = client.post("/posts/", json=post_data)

    new_post = resp.json()

    return new_post


@fixture
def token(dummy_user):
    access_token = o2.create_access_token(data={"user_id": dummy_user["id"]})

    return access_token


@fixture
def authorized_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"

    return client


@fixture
def dummy_posts(dummy_users, session):
    posts_data = []
    for user in dummy_users:
        post_data = {
            "title": f"{user.id} no. post",
            "content": "initial content",
            "owner_id": user.id,
        }
        posts_data.append(post_data)
    posts = [mo.Post(**post_data) for post_data in posts_data]
    session.add_all(posts)
    session.commit()

    return session.query(mo.Post).all()  # trap


@fixture
def dummy_users(session):
    users_data = []
    for i in range(6):
        user_data = {
            "email": f"user{i}@email.com",
            "password": f"pass{i}word",
        }
        users_data.append(user_data)
    users = [mo.User(**user_data) for user_data in users_data]
    session.add_all(users)
    session.commit()

    return session.query(mo.User).all()  # trap


@fixture
def dummy_vote(dummy_post, session, dummy_user):
    new_vote = mo.Vote(
        post_id=dummy_post["id"], user_id=dummy_user["id"], is_upvote=False
    )
    session.add(new_vote)
    session.commit()

    return new_vote
