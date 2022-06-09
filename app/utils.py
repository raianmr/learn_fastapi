from passlib.context import CryptContext


pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pass_ctx.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    return pass_ctx.verify(plain_password, hashed_password)
