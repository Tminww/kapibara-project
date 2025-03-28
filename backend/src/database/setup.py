from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.utils import database_logger as logger

# Настройка логирования


try:
    engine = create_async_engine(
        url=settings.DATABASE_URL,
        pool_size=20,  # Adjust pool size based on your workload
        max_overflow=10,  # Adjust maximum overflow connections
        pool_recycle=3600,  # Periodically recycle connections (optional)
        pool_pre_ping=True,  # Check the connection status before using it
    )

    async_session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,  # Отключаем автофлеш для явного контроля
    )
    logger.info(f"Подключение успешно")
except Exception as ex:
    logger.critical(f"Ошибка подключения: {ex}")


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше

    return wrapper


async def get_async_session():
    async with async_session_maker() as session:
        yield session
