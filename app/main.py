import psycopg2 as ppg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "welcome to my first api!"}


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(p: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**p.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    q = db.query(models.Post).filter(models.Post.id == id)
    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    q.delete()  # TODO read docs about the synchronize_session parameter
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, up: Post, db: Session = Depends(get_db)):
    q = db.query(models.Post).filter(models.Post.id == id)
    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )
    q.update(up.dict())
    db.commit()
    return {"data": q.first()}


if __name__ == "__main__":
    pass
