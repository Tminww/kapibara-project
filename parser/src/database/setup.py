import psycopg2
from dbconfig import get_settings
from log.createLogger import get_logger

logging = get_logger()


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
    logging.info("Успешное подключение к базе данных")
except Exception as e:
    logging.critical(f"Ошибка при подключении к базе данных {e}")


def get_sync_connection():
    if sync_connection:
        return sync_connection
