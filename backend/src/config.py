from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    BASE_DIR: Path = BASE_DIR

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    EXTERNAL_URL: str
    EXTERNAL_API_VERSION_PATH: str
    EXTERNAL_FILE_PATH: str

    PROXY: Optional[str] = None

    HOST: str
    PORT: int

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Настройки SMTP для отправки email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str = "your-app-name@your-domain.com"

    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    TESSERACT_CMD: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="ignore")

    @property
    def DATABASE_URL(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Config()
