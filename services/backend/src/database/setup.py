from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dbconfig import get_settings

import logging

logging.basicConfig(
    filename="./src/log/sqlalchemy.log",
    filemode="a",
    format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)
# logging.getLogger("sqlalchemy.orm").setLevel(logging.INFO)

settings = get_settings()

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    # echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    # echo=True,
)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

sync_session_maker = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all())


async def get_async_session():
    async with async_session_maker() as session:
        yield session
