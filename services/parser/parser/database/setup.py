import psycopg2
from parser.dbconfig import get_settings
from parser.log.createLogger import get_logger

logger = get_logger("database.setup")


settings = get_settings()

try:
    sync_connection = psycopg2.connect(
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
    sync_connection.autocommit = True
    logger.info(f"Успешное подключение к базе данных {settings.DB_NAME}")
except Exception as e:
    logger.critical(f"Ошибка при подключении к базе данных: {e}")


def get_sync_connection():
    if sync_connection:
        return sync_connection
