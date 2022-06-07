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
    pass


class PostUpdate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    pass


class UserUpdate(UserBase):
    pass
