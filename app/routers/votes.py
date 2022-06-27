from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models as mo
from .. import oauth2 as o2
from .. import schemas as sc
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cast_vote(
    v: sc.VoteCreate,
    db: Session = Depends(get_db),
    curr_u: mo.User = Depends(o2.get_current_user),
):
    q = db.query(mo.Vote).filter(
        mo.Vote.user_id == curr_u.id, mo.Vote.post_id == v.post_id
    )
    old_v: mo.Vote | None = q.first()

    if old_v:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {v.user_id} has already casted a vote on post {v.post_id}",
        )

    new_v_dict = {"post_id": v.post_id, "user_id": curr_u.id}
    if v.dir == sc.Direction.UPVOTE:
        new_v_dict["is_upvote"] = True
    elif v.dir == sc.Direction.DOWNVOTE:
        new_v_dict["is_upvote"] = False

    new_v = mo.Vote(**new_v_dict)
    db.add(new_v)
    db.commit()
    db.refresh(new_v)

    return new_v


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def uncast_vote(
    v: sc.VoteCreate,
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
            detail=f"user {v.user_id} didn't cast a vote on post {v.post_id}",
        )

    if v.user_id != curr_u.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
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
