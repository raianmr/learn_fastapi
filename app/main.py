from fastapi import FastAPI

from . import models as mo
from .config import settings as se
from .database import engine
from .routers import auth, posts, users, votes

mo.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "welcome to my first api!"}


# if __name__ == "__main__":
#     pass
