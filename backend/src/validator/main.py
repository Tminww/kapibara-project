import asyncio
from functools import wraps
import time
import requests
from PIL import Image
import pytesseract
import io
import logging
from typing import Dict, List, Optional, Union, Callable, Tuple
import re
from spellchecker import SpellChecker
from Levenshtein import ratio
from datetime import datetime, date
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from database import connection
from httpx import Response, Timeout, AsyncClient
from models import DocumentEntity
from config import settings
from utils import fetch

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

THRESHOLD = 90


class ValidationModule:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        self.spell = SpellChecker(language="ru")  # Инициализация проверки орфографии

    @connection
    async def get_documents_from_db(
        self,
        session: AsyncSession,
        start_date: Union[date, datetime, str],
        end_date: Union[date, datetime, str],
    ) -> List[Dict]:
        """Получает документы из базы данных на основе фильтров"""

        # Преобразование строковых дат в объекты date, если необходимо
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Подготовка основного запроса
        query = select(
            DocumentEntity.id,
            DocumentEntity.external_id,
            DocumentEntity.eo_number,
            DocumentEntity.complex_name,
            DocumentEntity.name,
            DocumentEntity.title,
            DocumentEntity.id_reg,
            DocumentEntity.id_type,
            DocumentEntity.is_valid,
        ).select_from(DocumentEntity)

        if start_date and end_date:
            # Использование объектов даты напрямую вместо функции to_date
            query = query.filter(DocumentEntity.view_date.between(start_date, end_date))

        # Добавляем order by и лимит
        query = query.order_by(DocumentEntity.document_date.desc())

        # Выполняем запрос
        result = await session.execute(query)
        documents = result.all()
        print(len(documents))
        # Преобразуем объекты SQLAlchemy в словари для дальнейшей обработки
        docs_as_dicts = []
        for doc in documents:
            doc_dict = {
                "id": doc[0],
                "external_id": doc[1],
                "eo_number": doc[2],
                "complex_name": doc[3],
                "name": doc[4],
                "title": doc[5],
                "id_reg": doc[6],
                "id_type": doc[7],
                "is_valid": doc[8],
            }
            docs_as_dicts.append(doc_dict)

        return docs_as_dicts

    async def get_image(self, document_id: str, page_number: int = 1) -> Image.Image:
        async with AsyncClient(proxy=settings.PROXY, timeout=Timeout(30.0)) as client:
            try:
                response: Response = await fetch(
                    client,
                    f"{settings.EXTERNAL_URL}/GetImage",
                    {
                        "documentId": document_id,
                        "pageNumper": page_number,
                    },
                )
                print(response)
                response.raise_for_status()
                return Image.open(io.BytesIO(response.content))
            except Exception as e:
                logger.error(f"Ошибка при загрузке изображения {document_id}: {e}")
            return None

    def extract_text_from_image(self, image: Image.Image) -> str:
        try:
            text = pytesseract.image_to_string(image, lang="rus")
            text = " ".join(text.split())
            return text.strip()
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}")
            return ""

    def clean_text(self, text: str) -> str:
        """Очистка текста от лишних символов и приведение к нижнему регистру"""
        text = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(text.split())

    def correct_text(self, text: str) -> str:
        """Исправление орфографических ошибок"""
        words = text.split()
        corrected = []
        for word in words:
            if self.spell.unknown([word]):
                corrected_word = self.spell.correction(word)
                corrected.append(corrected_word if corrected_word is not None else word)
            else:
                corrected.append(word)
        return " ".join(corrected)

    def compare_texts(self, db_text: str, ocr_text: str) -> Dict:
        """Сравнение текстов с поиском названия внутри OCR-текста"""
        # Очистка текстов
        db_clean = self.clean_text(db_text)
        ocr_clean = self.clean_text(ocr_text)

        # Поиск точного совпадения названия в OCR-тексте
        if db_clean in ocr_clean:
            similarity = 100.0
            is_valid = True
        else:
            # Нечёткое сравнение: найти фрагмент в OCR-тексте, который максимально похож на название
            max_similarity = 0.0
            db_words = db_clean.split()
            ocr_words = ocr_clean.split()
            len_db = len(db_words)

            for i in range(len(ocr_words) - len_db + 1):
                fragment = " ".join(ocr_words[i : i + len_db])
                sim = ratio(db_clean, fragment) * 100
                if sim > max_similarity:
                    max_similarity = sim

            similarity = max_similarity
            is_valid = similarity > THRESHOLD  # Порог валидности

        # Результат
        result = {
            "original_db": db_text,
            "original_ocr": ocr_text,
            "similarity_percent": round(similarity, 2),
            "is_valid": is_valid,
        }
        return result

    async def process_documents(
        self,
        start_date: str,
        end_date: str,
        progress_callback: Optional[Callable] = None,
    ) -> Dict:
        """
        Обрабатывает документы из базы данных на основе указанных фильтров.

        Args:
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации
            progress_callback: Функция для отслеживания прогресса (опционально)

        Returns:
            Dict: Статистика по обработанным документам
        """
        report_data = {
            "details": {},
            "summary": {
                "total": 0,
                "processed": 0,
                "validation_successful": 0,
                "validation_failed": 0,
                "failed": 0,
                "start_date": start_date,
                "end_date": end_date,
            },
        }

        # Получаем документы из базы данных
        documents = await self.get_documents_from_db(
            start_date=start_date,
            end_date=end_date,
        )

        if not documents:
            logger.warning("Не удалось получить документы из базы данных")
            if progress_callback:
                progress_callback(100, "Документы не найдены", report_data)

        total_documents = len(documents)
        report_data["summary"]["total"] = total_documents

        if progress_callback:
            progress_callback(
                10, f"Начало обработки {total_documents} документов", report_data
            )

        total_similarity = 0
        processed = 0

        for idx, doc in enumerate(documents):
            doc_id = doc.get("id")
            doc_ext_id = doc.get("external_id")
            doc_eo_number = doc.get("eo_number")
            if doc.get("name", None):
                db_text = doc.get("name")
            elif doc.get("complex_name", None):
                db_text = doc.get("complex_name")
            elif doc.get("title", None):
                db_text = doc.get("title")
            else:
                db_text = ""

            if progress_callback:
                progress = 10 + int(80 * (idx + 1) / report_data["summary"]["total"])
                progress_callback(
                    progress,
                    f"Обработка документа {idx+1}/{total_documents}",
                    report_data,
                )
            if doc.get("is_valid"):
                report_data["summary"]["validation_successful"] += 1
                continue

            if not doc_ext_id:
                logger.warning(f"Отсутствует внешний ID в документе: {doc_id}")
                report_data["summary"]["failed"] += 1
                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "DATABASE",
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": f"Отсутствует внешний ID",
                }
                continue

            # Обновляем прогресс

            # Получаем изображение первой страницы
            image = await self.get_image(doc_ext_id)
            if image is None:
                report_data["summary"]["failed"] += 1
                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "NETWORK",
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": "Не удалось получить изображение",
                }
                continue

            # Извлекаем текст из изображения
            ocr_text = self.extract_text_from_image(image)
            if not ocr_text:
                report_data["summary"]["failed"] += 1

                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "OCR",
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": "Не удалось извлечь текст из изображения",
                }
                continue

            # Сравниваем тексты
            try:
                comparison = self.compare_texts(db_text, ocr_text)
            except Exception as e:
                logger.error(f"Ошибка при сравнении текстов: {e}")
                report_data["summary"]["failed"] += 1
                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "COMPARISON",
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": str(e),
                }
                continue

            processed += 1
            report_data["summary"]["processed"] += 1

            total_similarity += comparison["similarity_percent"]

            # Подробная информация о документе
            doc_detail = {
                "doc_ext_id": doc_ext_id,
                "eo_number": doc_eo_number,
                "db_text": comparison["original_db"],
                "ocr_text": (
                    comparison["original_ocr"][:400] + "..."
                    if len(comparison["original_ocr"]) > 400
                    else comparison["original_ocr"]
                ),
                "similarity": comparison["similarity_percent"],
                "is_valid": comparison["is_valid"],
                "status": "success",
            }

            # Детальное логирование для каждого документа
            logger.info("Документ: %s", doc_detail)

            if comparison["is_valid"]:
                report_data["summary"]["validation_successful"] += 1
            else:
                report_data["summary"]["validation_failed"] += 1
                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "INVALID",
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": doc_detail,
                }

            if processed > 0:
                report_data["summary"]["average_similarity"] = round(
                    total_similarity / processed, 2
                )

        if progress_callback:
            progress_callback(
                100,
                f"Обработка завершена. Всего обработано {processed} / {total_documents} документов",
                report_data,
            )

        logger.info(f"Итоговая статистика: %s", report_data)


# Пример использования
if __name__ == "__main__":
    validator = ValidationModule()
    asyncio.run(validator.process_documents("2025-01-01", "2025-12-31", print))
