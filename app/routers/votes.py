from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models as mo
from .. import oauth2 as o2
from .. import schemas as sc
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sc.VoteRead)
async def cast_vote(
    v: sc.VoteCreate,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Post).filter(mo.Post.id == v.post_id)
    p: mo.Post | None = q.first()

    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    q = db.query(mo.Vote).filter(
        mo.Vote.user_id == curr_u.id, mo.Vote.post_id == v.post_id
    )
    old_v: mo.Vote | None = q.first()

    if old_v:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {curr_u.id} (currently logged in) has already casted a vote on post {v.post_id}",
        )

    # TODO raise when post not found

    new_v = mo.Vote(user_id=curr_u.id, **v.dict())
    db.add(new_v)
    db.commit()
    db.refresh(new_v)

    return new_v


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def uncast_vote(
    v: sc.VoteDelete,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Vote).filter(
        mo.Vote.user_id == curr_u.id, mo.Vote.post_id == v.post_id
    )
    old_v: mo.Vote | None = q.first()

    if not old_v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user {curr_u.id} (currently logged in) didn't cast a vote on post {v.post_id}",
        )

    q.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=list[sc.VoteRead])
async def get_votes(
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
    limit: int = 100,
    skip: int = 0,
):
    q = db.query(mo.Vote).limit(limit).offset(skip)
    all_p: list[mo.Vote] = q.all()

    return all_p


# TODO implement "change vote"
