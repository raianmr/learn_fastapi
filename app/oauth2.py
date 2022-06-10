from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models as mo
from . import oauth2 as o2
from . import schemas as sc
from . import utils as ut
from .database import engine, get_db

# openssl rand -hex 32
SECRET_KEY = "506caee9dc16a930c2a84ae7927d958749f43f04686fbee73ba6aa275607fb8e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    encodable = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    encodable["exp"] = expire_time

    encoded_jwt = jwt.encode(encodable, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> sc.TokenData:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = sc.TokenData(id=user_id)
    except JWTError as e:
        raise credentials_exception from e

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> mo.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user: mo.User = db.query(mo.User).filter(mo.User.id == token_data.id).first()  # type: ignore for now

    return user
