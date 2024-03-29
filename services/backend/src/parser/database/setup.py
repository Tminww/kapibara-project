import psycopg2 as db
from config import settings
from utils import utils

logger = utils.get_logger("database.setup")


try:
    sync_connection = db.connect(
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
    try:
        return sync_connection
    except Exception as ax:
        logger.critical(f"Ошибка при соединении с базой данных: {e}")
