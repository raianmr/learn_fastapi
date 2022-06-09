from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None
