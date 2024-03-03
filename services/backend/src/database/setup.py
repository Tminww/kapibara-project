from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dbconfig import get_settings

settings = get_settings()

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
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
