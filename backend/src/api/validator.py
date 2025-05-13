from fastapi import APIRouter, Body, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel
from typing import Annotated, Dict, List, Optional
from datetime import date, datetime
import json
from schemas import RequestValidatorStartSchema
from celery_worker import (
    celery,
    run_validator_task,
    VALIDATOR_STATUS_KEY,
    VALIDATOR_HISTORY_KEY,
    VALIDATOR_LAST_RUN_KEY,
)
from database import redis

router = APIRouter(prefix="/validator", tags=["validator"])


# Модели данных для API
class ValidatorStatus(BaseModel):
    task_id: Optional[str] = None
    state: str
    progress: int
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[float] = None
    report: Optional[Dict[str, dict]] = {}


class ValidatorTask(BaseModel):
    task_id: str
    status: str


class ValidatorHistory(BaseModel):
    history: List[ValidatorStatus]


@router.post("/start", response_model=ValidatorTask)
async def start_validator(
    params: RequestValidatorStartSchema,
):
    """Запуск парсера в фоновом режиме."""
    print(params)
    # Проверяем, не запущен ли уже парсер
    status_data = redis.get(VALIDATOR_STATUS_KEY)
    if status_data:
        status = json.loads(status_data)
        if status.get("state") in ["STARTED", "PROGRESS"]:
            task_id = status.get("task_id")
            task_result = celery.AsyncResult(task_id)

            if not task_result.ready():
                return ValidatorTask(
                    task_id=task_id,
                    status="Проверка данных уже запущена и выполняется.",
                )

    print(params.send_email, params.recipient_email)
    # Запуск задачи с передачей параметров start_date и end_date
    task = run_validator_task.delay(
        start_date=params.start_date,
        end_date=params.end_date,
        send_email=params.send_email,
        recipient_email=params.recipient_email,
    )

    return ValidatorTask(task_id=task.id, status="Проверка данных запущена.")


@router.get("/status", response_model=ValidatorStatus)
async def get_validator_status():
    """Получение текущего статуса парсера."""

    status_data = redis.get(VALIDATOR_STATUS_KEY)

    if not status_data:
        return ValidatorStatus(
            state="UNKNOWN",
            progress=0,
            status="Проверка данных еще не запускалась или данные о статусе отсутствуют.",
        )

    status = json.loads(status_data)

    return ValidatorStatus(**status)


@router.post("/stop", response_model=ValidatorTask)
async def stop_validator():
    """Остановка выполняющейся проверки."""

    status_data = redis.get(VALIDATOR_STATUS_KEY)

    if not status_data:
        raise HTTPException(
            status_code=404, detail="Нет данных о работающей проверке данных."
        )

    status_data = json.loads(status_data)

    if status_data.get("state") not in ["STARTED", "PROGRESS"]:
        raise HTTPException(
            status_code=400, detail="Проверка данных не выполняется в данный момент."
        )

    task_id = status_data.get("task_id")
    if not task_id:
        raise HTTPException(
            status_code=500, detail="Не удалось определить ID задачи проверки данных."
        )

    # Отмена задачи
    celery.control.revoke(task_id, terminate=True)

    # Обновление статуса в Redis
    status_data["state"] = "REVOKED"
    status_data["status"] = "Проверка данных была остановлена пользователем"
    status_data["end_time"] = datetime.now().isoformat()

    redis.set(VALIDATOR_STATUS_KEY, json.dumps(status_data))
    redis.lpush(VALIDATOR_HISTORY_KEY, json.dumps(status_data))
    redis.ltrim(VALIDATOR_HISTORY_KEY, 0, 49)

    return ValidatorTask(task_id=task_id, status="Проверка данных остановлена.")


@router.get("/history", response_model=ValidatorHistory)
async def get_validator_history(limit: int = 10):
    """Получение истории выполнения проверки."""

    history_data = redis.lrange(VALIDATOR_HISTORY_KEY, 0, limit - 1)

    if not history_data:
        return ValidatorHistory(history=[])

    history = [json.loads(item) for item in history_data]

    return ValidatorHistory(history=history)


@router.get("/last-run", response_model=ValidatorStatus)
async def get_last_report():
    """Получение отчета о последнем выполнении проверки."""

    report_data = redis.get(VALIDATOR_LAST_RUN_KEY)

    if not report_data:
        raise HTTPException(
            status_code=404,
            detail="Отчет о последнем выполнении проверки данных отсутствует.",
        )

    report = json.loads(report_data)

    return report
