import logging


def get_logger() -> None:
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    # создаем обработчик для файла и
    # установим уровень отладки
    ch = logging.FileHandler("./log/dataBase.log", "a")
    ch.setLevel(logging.INFO)

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

logger = get_logger()