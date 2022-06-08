from passlib.context import CryptContext


pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pass_ctx.hash(password)
