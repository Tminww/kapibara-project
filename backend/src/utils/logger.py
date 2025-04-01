from config import settings
import logging
from datetime import datetime


def get_logger(logger_name: str, file_name: str = "logger") -> logging:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # создаем обработчик для файла и
    # установим уровень отладки
    ch = logging.FileHandler(f"{settings.BASE_DIR}/log/{file_name}.log", "a")
    # ch.setLevel(logging.DEBUG)

    # строка формата сообщения
    strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
    # строка формата времени
    datefmt = "%Y-%m-%d %H:%M:%S"
    # создаем форматтер
    formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

    # добавляем форматтер к 'ch'
    ch.setFormatter(formatter)
    # добавляем ch в регистратор
    logger.addHandler(ch)
    # вызов функций, регистрирующих
    # события в коде
    return logger  # type: ignore


timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
parser_logger = get_logger(logger_name="parser", file_name="parser")
backend_logger = get_logger(logger_name="backend", file_name="backend")
database_logger = get_logger("sqlalchemy.engine", "database")
