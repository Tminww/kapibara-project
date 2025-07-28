"""
Планировщик задач с использованием существующих Pydantic схем
"""
import requests
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from config import settings
from schemas import RequestValidatorStartSchema

WAIT_TIME = 1800 # 30 минут

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(getattr(settings, 'LOG_FILE', f'{settings.BASE_DIR}/log/scheduler.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.base_url = f"{settings.HOST_SCHEME}://{settings.HOST}:{settings.PORT}/api"
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def start_parser(self) -> dict:
        """Запуск парсера"""
        logger.info("🚀 Запуск парсера...")
        
        response = self.session.post(
            f"{self.base_url}/parser/start",
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result
    
    def status_parser(self) -> dict:
        """Запуск парсера"""
        logger.info("🚀 Проверка статуса парсера...")
        
        response = self.session.get(
            f"{self.base_url}/parser/status",
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return result
    
    def start_validator(self) -> dict:
        """Запуск валидатора с использованием Pydantic схемы"""
        logger.info("🚀 Запуск валидатора...")
        
        # Создаем объект схемы с данными
        validator_params = RequestValidatorStartSchema(
            start_date=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            send_email=getattr(settings, 'SEND_EMAIL', True),
            recipient_email=getattr(settings, 'RECIPIENT_EMAIL', 'admin@example.com')
        )
        
        # Конвертируем в dict для отправки
        data = validator_params.model_dump()
        
        response = self.session.post(
            f"{self.base_url}/validator/start",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"✅ Валидатор запущен: {result} - {validator_params.start_date} до {validator_params.end_date}")
        return result
    
    def run_scheduled_tasks(self):
        """Основной метод"""
        logger.info("=== Начало выполнения запланированных задач ===")
        
        try:
            # 1. Запуск парсера
            parser_result = self.start_parser()
            time.sleep(10)  # Небольшая задержка для стабилизации
            status = self.status_parser()
            if status.get("state") in ["STARTED", "PROGRESS"]:
                logger.info(f"✅ Парсер запущен: {status.get('task_id')}")
            else:
                logger.error("❌ Ошибка при запуске парсера")
                return
            
            while True:
                status = self.status_parser()
                if status.get("state") not in ["STARTED", "PROGRESS"]:
                    break
                logger.info(f"Текущий статус: {status['state']}. Ожидание...")
                      
                # 2. Ожидание
                logger.info(f"⏳ Ожидание {WAIT_TIME // 60} минут...")
                time.sleep(WAIT_TIME)
            
            
            # 3. Запуск валидатора
            validator_result = self.start_validator()
            
            logger.info("✅ Все задачи успешно запущены")
            
        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            raise

def main():
    """Точка входа"""
    lock_file = Path(f'{settings.BASE_DIR}/scripts/scheduler.lock')
    
    if lock_file.exists():
        logger.warning("Планировщик уже запущен")
        return
    
    try:
        lock_file.touch()
        scheduler = TaskScheduler()
        scheduler.run_scheduled_tasks()
    finally:
        if lock_file.exists():
            lock_file.unlink()

if __name__ == "__main__":
    main()