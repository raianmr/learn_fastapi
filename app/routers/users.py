from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models as mo
from .. import schemas as sc
from .. import utils as ut
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[sc.UserRead])
async def get_users(db: Session = Depends(get_db)):
    q = db.query(mo.User)
    all_u: list[mo.User] = q.all()

    return all_u


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sc.UserRead)
async def create_user(u: sc.UserCreate, db: Session = Depends(get_db)):
    q = db.query(mo.User).filter(mo.User.email == u.email)
    existing_u: mo.User | None = q.first()

    if existing_u:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with email {u.email} already exists",
        )

    hashed_pass = ut.hash(u.password)
    u.password = hashed_pass
    new_u = mo.User(**u.dict())
    db.add(new_u)
    db.commit()
    db.refresh(new_u)

    return new_u


@router.get("/{id}", response_model=sc.UserRead)
async def get_user(id: int, db: Session = Depends(get_db)):
    q = db.query(mo.User).filter(mo.User.id == id)
    u: mo.User | None = q.first()

    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} was not found",
        )

    return u
