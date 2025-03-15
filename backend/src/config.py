import os
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)


class DBConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.db.env")

    @property
    def DATABASE_URL(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class ExternalApiConfig(BaseSettings):
    EXTERNAL_URL: str
    EXTERNAL_API_VERSION_PATH: str
    EXTERNAL_FILE_PATH: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.external.env")


class Settings:
    BASE_DIR = BASE_DIR
    db = DBConfig()
    external = ExternalApiConfig()


settings = Settings()
