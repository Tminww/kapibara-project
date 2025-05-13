# parser_router.py
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from fastapi.responses import JSONResponse
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from celery_worker import (
    celery,
    run_parser_task,
    PARSER_STATUS_KEY,
    PARSER_HISTORY_KEY,
    PARSER_LAST_RUN_KEY,
)
from database import redis
from config import settings

router = APIRouter(prefix="/parser", tags=["Parser"])


# Модели данных для API
class ParserStatus(BaseModel):
    task_id: Optional[str] = None
    state: str
    progress: int
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[float] = None
    report: Optional[Dict[str, dict]] = {}


class ParserTask(BaseModel):
    task_id: str
    status: str


class ParserHistory(BaseModel):
    history: List[ParserStatus]


@router.post("/start", response_model=ParserTask)
async def start_parser():
    """Запуск парсера в фоновом режиме."""

    # Проверяем, не запущен ли уже парсер
    status_data = redis.get(PARSER_STATUS_KEY)
    if status_data:
        status = json.loads(status_data)
        if status.get("state") in ["STARTED", "PROGRESS"]:
            task_id = status.get("task_id")
            task_result = celery.AsyncResult(task_id)

            if not task_result.ready():
                return ParserTask(
                    task_id=task_id, status="Сбор данных уже запущен и выполняется."
                )

    # Запуск задачи
    task = run_parser_task.delay()

    return ParserTask(task_id=task.id, status="Сбор данных запущен.")


@router.get("/status", response_model=ParserStatus)
async def get_parser_status():
    """Получение текущего статуса парсера."""

    status_data = redis.get(PARSER_STATUS_KEY)

    if not status_data:
        return ParserStatus(
            state="UNKNOWN",
            progress=0,
            status="Сбор данных еще не запускался или данные о статусе отсутствуют.",
        )

    status = json.loads(status_data)

    return ParserStatus(**status)


@router.post("/stop", response_model=ParserTask)
async def stop_parser():
    """Остановка выполняющегося парсера."""

    status_data = redis.get(PARSER_STATUS_KEY)

    if not status_data:
        raise HTTPException(
            status_code=404, detail="Нет данных о работающем сборе данных."
        )

    status_data = json.loads(status_data)

    if status_data.get("state") not in ["STARTED", "PROGRESS"]:
        raise HTTPException(
            status_code=400, detail="Сбор данных не выполняется в данный момент."
        )

    task_id = status_data.get("task_id")
    if not task_id:
        raise HTTPException(
            status_code=500, detail="Не удалось определить ID задачи сбора данных."
        )

    # Отмена задачи
    celery.control.revoke(task_id, terminate=True)

    # Обновление статуса в Redis
    status_data["state"] = "REVOKED"
    status_data["status"] = "Сбор данных был остановлен пользователем"
    status_data["end_time"] = datetime.now().isoformat()

    redis.set(PARSER_STATUS_KEY, json.dumps(status_data))
    redis.lpush(PARSER_HISTORY_KEY, json.dumps(status_data))
    redis.ltrim(PARSER_HISTORY_KEY, 0, 49)

    return ParserTask(task_id=task_id, status="Сбор данных остановлен.")


@router.get("/history", response_model=ParserHistory)
async def get_parser_history(limit: int = 10):
    """Получение истории выполнения парсера."""

    history_data = redis.lrange(PARSER_HISTORY_KEY, 0, limit - 1)

    if not history_data:
        return ParserHistory(history=[])

    history = [json.loads(item) for item in history_data]

    return ParserHistory(history=history)


@router.get("/last-run", response_model=ParserStatus)
async def get_last_report():
    """Получение отчета о последнем выполнении парсера."""

    report_data = redis.get(PARSER_LAST_RUN_KEY)

    if not report_data:
        raise HTTPException(
            status_code=404,
            detail="Отчет о последнем выполнении сбора данных отсутствует.",
        )

    report = json.loads(report_data)

    return report
