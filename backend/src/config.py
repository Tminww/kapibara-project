from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os

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

    HOST_SCHEME: Literal['http', 'https'] = "http" # или "https"
    HOST: str
    PORT: int
    CURRENT_IP: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Настройки SMTP для отправки email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str = "your-app-name@your-domain.com"

    TESSERACT_CMD: str

    model_config = SettingsConfigDict(
        # Убираем жесткую привязку к файлу .env
        env_file=f"{BASE_DIR}/../.env" if os.path.exists(f"{BASE_DIR}/../.env") else None,
        extra="ignore",
        # Добавляем чтение из переменных окружения как приоритет
        env_file_encoding='utf-8'
    )

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CELERY_BROKER_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_RESULT_BACKEND(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache()
def get_settings():
    return Config()


settings = get_settings()