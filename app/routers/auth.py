from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models as mo
from .. import oauth2 as o2
from .. import schemas as sc
from .. import utils as ut
from ..database import engine, get_db

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=sc.Token)
async def login(
    creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user: mo.User | None = (
        db.query(mo.User).filter(mo.User.email == creds.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!"
        )

    if not ut.verify(creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials!"
        )

    access_token = o2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
