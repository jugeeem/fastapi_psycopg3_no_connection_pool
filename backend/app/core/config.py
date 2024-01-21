import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn

# .envファイルの内容を読み込む
load_dotenv()


class Config:
    # DB接続情報
    DATABASE_DBNAME: str = os.getenv("DATABASE_DBNAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_URL: Optional[
        PostgresDsn
    ] = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DBNAME}"

    # prefix
    API_V1_STR: str = "/api/v1"
    TODO_PREFIX: str = "/todo"


config = Config()
