from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from utils import database_logger as logger

# Настройка логирования


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


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper


async def get_async_session():
    async with async_session_maker() as session:
        yield session
