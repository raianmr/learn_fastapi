from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models as mo
from .. import oauth2 as o2
from .. import schemas as sc
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[sc.PostRead])
async def get_posts(
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: str = "",
):
    print(limit)

    q = (
        db.query(mo.Post)
        .filter(mo.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    )
    all_p: list[mo.Post] = q.all()

    return all_p


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sc.PostRead)
async def create_posts(
    p: sc.PostCreate,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    new_p = mo.Post(owner_id=curr_u.id, **p.dict())
    db.add(new_p)
    db.commit()
    db.refresh(new_p)

    return new_p


@router.get("/{id}", response_model=sc.PostRead)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Post).filter(mo.Post.id == id)
    p: mo.Post | None = q.first()

    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    return p


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Post).filter(mo.Post.id == id)
    p: mo.Post | None = q.first()

    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if p.owner_id != curr_u.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )

    q.delete()  # TODO read docs about the synchronize_session parameter
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=sc.PostRead)
async def update_post(
    id: int,
    up: sc.PostUpdate,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Post).filter(mo.Post.id == id)
    p: mo.Post | None = q.first()

    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if p.owner_id != curr_u.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )

    q.update(up.dict())
    db.commit()

    return p
