from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    pass
