from pydantic import BaseSettings


class Settings(BaseSettings):
    db_type: str = ""
    db_host: str = ""
    db_name: str = ""
    db_port: str = ""
    db_pass: str = ""
    db_user: str = ""

    dur_in_mins: int = 0
    secret_key: str = ""
    hash_algo: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
