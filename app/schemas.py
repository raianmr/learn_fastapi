from datetime import datetime
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

class PostWithVotes(BaseModel):
    Post: PostRead
    score: int

class PostUpdate(PostBase):
    pass


class VoteBase(BaseModel):
    post_id: int
    user_id: int


class VoteCreate(BaseModel):
    post_id: int
    is_upvote: bool


class VoteRead(VoteBase):
    is_upvote: bool

    class Config:
        orm_mode = True


class VoteUpdate(VoteCreate):
    pass


class VoteDelete(BaseModel):
    post_id: int
