from turtle import pos
from typing import Iterator

import psycopg2 as ppg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from time import sleep

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = ppg2.connect(
            host="localhost",
            database="fapi_lrn",
            user="fapi_lrnr",
            password="fapi_lrnr",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        break
    except Exception as err:
        print(err)
        sleep(3)


def get_id() -> Iterator[int]:
    for i in range(69, 420):
        yield i


id_gen = get_id()
my_posts: list[dict] = []


def find_post_index(id: int) -> int:
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return -1


@app.get("/")
async def root():
    return {"message": "welcome to my first api!"}


@app.get("/posts")
async def get_posts():
    cursor.execute(
        """SELECT * FROM posts """
    )
    posts = cursor.fetchall()
    return {"data": posts}

# order is vvi
# @app.get("/posts/latest")
# async def get_latest_post():
#     post = my_posts[-1]
#     return {"post-details": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s """,
        (id, )
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    return {"post_details": post}


@app.put("/posts/{id}")
async def update_post(id: int, p: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
        (p.title, p.content, p.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """,
        (id, )
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(p: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (p.title, p.content, p.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


if __name__ == "__main__":
    pass
