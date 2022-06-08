from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models as mo
from .. import schemas as sc
from .. import utils as ut
from ..database import engine, get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[sc.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(mo.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sc.Post)
async def create_posts(p: sc.PostCreate, db: Session = Depends(get_db)):
    new_post = mo.Post(**p.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=sc.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(mo.Post).filter(mo.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    q = db.query(mo.Post).filter(mo.Post.id == id)

    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    q.delete()  # TODO read docs about the synchronize_session parameter
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=sc.Post)
async def update_post(id: int, up: sc.PostUpdate, db: Session = Depends(get_db)):
    q = db.query(mo.Post).filter(mo.Post.id == id)

    if not q.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    q.update(up.dict())
    db.commit()

    return q.first()
