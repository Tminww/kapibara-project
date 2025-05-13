from celery import Celery, Task
import json
from datetime import datetime
import asyncio
from typing import Dict, List, Optional, Union
from database import redis
from parser import parse
from config import settings
from validator import ValidationModule
from notificator import EmailNotificator

# Настройка Celery
celery: Celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
)

# Статус последнего запуска
PARSER_STATUS_KEY = "parser:status"
PARSER_HISTORY_KEY = "parser:history"
PARSER_LAST_RUN_KEY = "parser:last_run"

# Ключи для хранения статуса в Redis
VALIDATOR_STATUS_KEY = "validation:status"
VALIDATOR_HISTORY_KEY = "validation:history"
VALIDATOR_LAST_RUN_KEY = "validation:last_run"


@celery.task(bind=True)
def run_parser_task(self: Task):
    """Задача Celery для запуска парсера с обновлением статуса."""
    # Начальное состояние
    self.update_state(
        state="STARTED", meta={"progress": 0, "status": "Начало сбора данных"}
    )
    task_id = self.request.id
    start_time = datetime.now().isoformat()
    duration = lambda: (
        datetime.fromisoformat(datetime.now().isoformat())
        - datetime.fromisoformat(start_time)
    ).total_seconds()

    # Обновление в Redis
    with celery.backend.client.pipeline() as pipe:
        pipe.set(
            PARSER_STATUS_KEY,
            json.dumps(
                {
                    "state": "STARTED",
                    "progress": 0,
                    "status": "Начало сбора данных",
                    "task_id": task_id,
                    "start_time": start_time,
                    "duration": duration(),
                    "report": {},
                }
            ),
        )
        pipe.execute()

    try:

        def progress_callback(progress: int, status: str, report: dict = {}):
            """Обновление состояния задачи и Redis."""
            self.update_state(
                state="PROGRESS", meta={"progress": progress, "status": status}
            )
            with celery.backend.client.pipeline() as pipe:
                pipe.set(
                    PARSER_STATUS_KEY,
                    json.dumps(
                        {
                            "state": "PROGRESS",
                            "progress": progress,
                            "status": status,
                            "task_id": task_id,
                            "start_time": start_time,
                            "duration": duration(),
                            "report": report,
                        }
                    ),
                )
                pipe.execute()

        # Запуск парсера с отслеживанием прогресса и возвращением отчета
        asyncio.run(parse(progress_callback=progress_callback))

        end_time = datetime.now().isoformat()
        result = redis.get(PARSER_STATUS_KEY)
        result = json.loads(result)
        result["state"] = "SUCCESS"
        result["end_time"] = end_time

        # Сохранение результата в Redis
        with celery.backend.client.pipeline() as pipe:
            pipe.set(PARSER_STATUS_KEY, json.dumps(result))
            pipe.set(PARSER_LAST_RUN_KEY, json.dumps(result))
            pipe.lpush(PARSER_HISTORY_KEY, json.dumps(result))
            pipe.ltrim(
                PARSER_HISTORY_KEY, 0, 49
            )  # Хранить только последние 50 запусков
            pipe.execute()

    except Exception as e:
        end_time = datetime.now().isoformat()
        result = redis.get(PARSER_STATUS_KEY)
        result = json.loads(result)
        result["state"] = "FAILURE"
        result["status"] = f"Ошибка на сервере при получении данных"
        result["end_time"] = end_time

        # Сохранение ошибки в Redis
        with celery.backend.client.pipeline() as pipe:
            pipe.set(PARSER_STATUS_KEY, json.dumps(result))
            pipe.set(PARSER_LAST_RUN_KEY, json.dumps(result))
            pipe.lpush(PARSER_HISTORY_KEY, json.dumps(result))
            pipe.ltrim(PARSER_HISTORY_KEY, 0, 49)
            pipe.execute()

        raise


@celery.task(bind=True)
def run_validator_task(
    self: Task,
    start_date: str,
    end_date: str,
    send_email: bool,
    recipient_email: str,
):
    """
    Celery задача для запуска процесса валидации документов.

    Args:
        start_date (str): Начальная дата в формате 'YYYY-MM-DD'
        end_date (str): Конечная дата в формате 'YYYY-MM-DD'
        email_notification (bool): Флаг отправки уведомления по email
        recipient_email (str): Email получателя уведомления

    Returns:
        Dict: Результаты валидации
    """
    # Начальное состояние
    self.update_state(
        state="STARTED",
        meta={"progress": 0, "status": "Инициализация модуля валидации"},
    )

    task_id = self.request.id
    start_time = datetime.now().isoformat()
    duration = lambda: (
        datetime.fromisoformat(datetime.now().isoformat())
        - datetime.fromisoformat(start_time)
    ).total_seconds()

    # Обновление в Redis
    with celery.backend.client.pipeline() as pipe:
        pipe.set(
            VALIDATOR_STATUS_KEY,
            json.dumps(
                {
                    "state": "STARTED",
                    "progress": 0,
                    "status": "Начало проверки",
                    "task_id": task_id,
                    "start_time": start_time,
                    "duration": duration(),
                    "report": {},
                }
            ),
        )
        pipe.execute()

    try:

        def progress_callback(progress: int, status: str, report: dict = {}):
            """Обновление состояния задачи и Redis."""
            self.update_state(
                state="PROGRESS", meta={"progress": progress, "status": status}
            )
            with celery.backend.client.pipeline() as pipe:
                pipe.set(
                    VALIDATOR_STATUS_KEY,
                    json.dumps(
                        {
                            "state": "PROGRESS",
                            "progress": progress,
                            "status": status,
                            "task_id": task_id,
                            "start_time": start_time,
                            "duration": duration(),
                            "report": report,
                        }
                    ),
                )
                pipe.execute()

        # Запуск проверки с отслеживанием прогресса и возвращением отчета
        validator = ValidationModule()
        asyncio.run(
            validator.process_documents(start_date, end_date, progress_callback)
        )

        end_time = datetime.now().isoformat()
        result = redis.get(VALIDATOR_STATUS_KEY)
        result = json.loads(result)
        result["state"] = "SUCCESS"
        result["end_time"] = end_time

        # Сохранение результата в Redis
        with celery.backend.client.pipeline() as pipe:
            pipe.set(VALIDATOR_STATUS_KEY, json.dumps(result))
            pipe.set(VALIDATOR_LAST_RUN_KEY, json.dumps(result))
            pipe.lpush(VALIDATOR_HISTORY_KEY, json.dumps(result))
            pipe.ltrim(
                VALIDATOR_HISTORY_KEY, 0, 49
            )  # Хранить только последние 50 запусков
            pipe.execute()

        # Отправка уведомления по email при успешном завершении
        if send_email:
            run_notificator.delay(
                result, notification_type="email", recipient_email=recipient_email
            )

    except Exception as e:
        end_time = datetime.now().isoformat()
        result = redis.get(VALIDATOR_STATUS_KEY)
        result = json.loads(result)
        result["state"] = "FAILURE"
        result["status"] = f"Ошибка на сервере при проверке данных"
        result["end_time"] = end_time

        # Сохранение ошибки в Redis
        with celery.backend.client.pipeline() as pipe:
            pipe.set(VALIDATOR_STATUS_KEY, json.dumps(result))
            pipe.set(VALIDATOR_LAST_RUN_KEY, json.dumps(result))
            pipe.lpush(VALIDATOR_HISTORY_KEY, json.dumps(result))
            pipe.ltrim(VALIDATOR_HISTORY_KEY, 0, 49)
            pipe.execute()

        # Отправка уведомления о неудаче
        if send_email:
            run_notificator.delay(
                result, notification_type="email", recipient_email=recipient_email
            )

        raise


@celery.task(bind=True)
def run_notificator(
    self: Task,
    data: Union[Dict, List[Dict]],
    notification_type: str = "email",
    recipient_email: str = "serafim.57775@gmail.com",
):
    """
    Celery задача для отправки уведомлений пользователям.

    Args:
        data (Union[Dict, List[Dict]]): Данные для уведомления
        notification_type (str): Тип уведомления (email, sms, etc.)
        recipient_email (str): Email получателя
    Returns:
        Dict: Результаты уведомления
    """
    task_id = self.request.id
    print(f"Запуск задачи уведомления: {task_id}")
    self.update_state(
        state="STARTED",
        meta={"progress": 0, "status": "Подготовка уведомления"},
    )

    try:
        if notification_type == "email":
            # Импортируем EmailNotificator здесь, чтобы избежать циклических импортов
            from notificator import EmailNotificator

            # Создаем экземпляр отправителя email
            notifier = EmailNotificator()

            # Определяем тему письма в зависимости от статуса операции
            if isinstance(data, dict):
                state = data.get("state", "UNKNOWN")
                status_text = (
                    "успешно завершена"
                    if state == "SUCCESS"
                    else "завершена с ошибками"
                )
                operation_type = (
                    "валидации"
                    if "validation" in data.get("task_id", "")
                    else "обработки"
                )
                subject = f"Отчет о результатах {operation_type} данных - {status_text}"

                # Создаем HTML-контент для отчета
                html_content = notifier.format_validation_report(data)

                # Генерируем отчет в формате JSON для вложения
                report_json = json.dumps(data, indent=4, ensure_ascii=False)
                attachments = {"validation_report.json": report_json.encode("utf-8")}

                # Отправляем письмо
                self.update_state(
                    state="PROGRESS",
                    meta={"progress": 50, "status": "Отправка уведомления"},
                )

                # Добавим логирование для отладки
                print(f"Отправка email на адрес: {recipient_email}")
                print(f"Тема письма: {subject}")

                # Отправляем уведомление
                result = notifier.send_email(
                    to_email=recipient_email,
                    subject=subject,
                    body=html_content,
                    attachments=attachments,
                )

                print(f"Результат отправки: {result}")

            else:  # если data это список словарей
                # Здесь можно реализовать отправку сводного отчета по всем заданиям
                pass

            self.update_state(
                state="SUCCESS",
                meta={"progress": 100, "status": "Уведомление успешно отправлено"},
            )

            return {
                "success": True,
                "notification_type": notification_type,
                "recipient": recipient_email,
                "timestamp": datetime.now().isoformat(),
            }

        elif notification_type == "sms":
            # Здесь можно реализовать отправку SMS-уведомлений
            pass

        else:
            raise ValueError(f"Неподдерживаемый тип уведомления: {notification_type}")

    except Exception as e:
        import traceback

        error_trace = traceback.format_exc()
        print(f"Ошибка при отправке уведомления: {str(e)}")
        print(f"Трассировка: {error_trace}")

        self.update_state(
            state="FAILURE",
            meta={
                "progress": 0,
                "status": f"Ошибка при отправке уведомления: {str(e)}",
            },
        )

        return {
            "success": False,
            "error": str(e),
            "notification_type": notification_type,
            "recipient": recipient_email,
            "timestamp": datetime.now().isoformat(),
        }
