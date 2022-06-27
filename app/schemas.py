from datetime import datetime
from enum import IntEnum, unique
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


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


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserRead

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass


@unique
class Direction(IntEnum):
    UPVOTE = 1
    DOWNVOTE = -1


class VoteBase(BaseModel):
    post_id: int
    user_id: int
    dir: Direction


class VoteCreate(VoteBase):
    pass


class VoteRead(BaseModel):
    post_id: int
    user_id: int
    is_upvote: bool

    class Config:
        orm_mode = True
        # use_enum_values = True  # unsure if needed


class VoteUpdate(VoteBase):
    pass
