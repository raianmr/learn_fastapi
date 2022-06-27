from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models as mo
from . import schemas as sc
from .config import settings as se
from .database import get_db

# openssl rand -hex 32
SECRET_KEY = se.secret_key
ALGORITHM = se.hash_algo
ACCESS_TOKEN_EXPIRE_MINUTES = se.dur_in_mins


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
