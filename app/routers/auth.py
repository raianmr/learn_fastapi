from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from .. import models as mo
from .. import schemas as sc
from .. import utils as ut
from ..database import engine, get_db

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
async def login(creds: sc.UserLogin, db: Session = Depends(get_db)):
    user = db.query(mo.User).filter(mo.User.email == creds.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials!"
        )

    if not ut.verify(creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials!"
        )

    # create token
    # return token

    return {"token": "dummy token"}
