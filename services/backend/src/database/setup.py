from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from utils.utils import get_logger
import logging

logger = get_logger(logger_name="database", file_name="backend")

logging.basicConfig(
    filename="./src/log/sqlalchemy.log",
    filemode="a",
    format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
# logging.getLogger("sqlalchemy.orm").setLevel(logging.INFO)


try:
    sync_engine = create_engine(
        url=settings.DATABASE_URL_psycopg,
        echo=True,
        # pool_size=5,
        # max_overflow=10,
    )

    async_engine = create_async_engine(
        url=settings.DATABASE_URL,
        # echo=True,
    )

    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

    sync_session_maker = sessionmaker(sync_engine)
    logger.info(f"Подключение успешно")
except Exception as ex:
    logger.critical(f"Ошибка подключения: {ex}")


async def get_async_session():
    async with async_session_maker() as session:
        yield session
