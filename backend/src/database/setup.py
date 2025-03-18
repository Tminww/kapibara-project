from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from utils import backend_logger as logger


try:
    engine = create_async_engine(
        url=settings.DATABASE_URL,
        # echo=True,
    )

    async_session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )
    logger.info(f"Подключение успешно")
except Exception as ex:
    logger.critical(f"Ошибка подключения: {ex}")


async def get_async_session():
    async with async_session_maker() as session:
        yield session
