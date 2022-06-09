from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models as mo
from .. import schemas as sc
from .. import utils as ut
from ..database import engine, get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[sc.UserRead])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(mo.User).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sc.UserRead)
async def create_users(u: sc.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = ut.hash(u.password)
    u.password = hashed_pass

    new_user = mo.User(**u.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=sc.UserRead)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(mo.User).filter(mo.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} was not found",
        )

    return user
