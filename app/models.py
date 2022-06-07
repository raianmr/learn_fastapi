from .database import Base


class Post(Base):
    __tablename__ = "posts"
    title: str
    content: str
    published: bool = True
