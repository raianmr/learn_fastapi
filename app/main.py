import psycopg2 as ppg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models as mo
from . import schemas as sc
from .database import engine, get_db

mo.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my first api!"}


@app.get("/posts", response_model=list[sc.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(mo.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=sc.Post)
async def create_posts(p: sc.PostCreate, db: Session = Depends(get_db)):
    new_post = mo.Post(**p.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", response_model=sc.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(mo.Post).filter(mo.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    q = db.query(mo.Post).filter(mo.Post.id == id)

    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )

    q.delete()  # TODO read docs about the synchronize_session parameter
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=sc.Post)
async def update_post(id: int, up: sc.PostUpdate, db: Session = Depends(get_db)):
    q = db.query(mo.Post).filter(mo.Post.id == id)

    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"post with id {id} was not found"
        )

    q.update(up.dict())
    db.commit()

    return q.first()


# everything user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=sc.User)
async def create_users(u: sc.UserCreate, db: Session = Depends(get_db)):
    new_user = mo.User(**u.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


if __name__ == "__main__":
    pass
