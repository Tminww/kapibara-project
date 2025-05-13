from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from redis import Redis
from contextlib import asynccontextmanager
import asyncio

from config import settings
from utils import database_logger as logger

# Соединение с Redis (это ОК, так как Redis синхронный)
redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


# Функция для создания engine в текущем цикле событий
async def create_db_engine():
    try:
        engine = create_async_engine(
            url=settings.DATABASE_URL,
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
            pool_pre_ping=True,
        )
        logger.info("Подключение успешно создано")
        return engine
    except Exception as ex:
        logger.critical(f"Ошибка подключения: {ex}")
        raise


# Функция для создания session_maker в текущем цикле событий
async def create_session_maker():
    engine = await create_db_engine()
    return (
        async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=False,
        ),
        engine,
    )


# Для использования в FastAPI
@asynccontextmanager
async def get_async_session():
    session_maker, engine = await create_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await engine.dispose()


# Декоратор для использования в обычных асинхронных функциях
def connection(method):
    async def wrapper(*args, **kwargs):
        session_maker, engine = await create_session_maker()
        async with session_maker() as session:
            try:
                async with session.begin():
                    result = await method(*args, session=session, **kwargs)
                return result
            except Exception as e:
                raise e
            finally:
                await engine.dispose()  # Важно закрывать engine!

    return wrapper
