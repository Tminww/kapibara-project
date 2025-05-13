from functools import wraps
import time
import requests
from PIL import Image
import pytesseract
import io
import logging
from urllib.parse import urlencode
from typing import Dict, List
import re
from Levenshtein import ratio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Настройки
class Settings:
    EXTERNAL_URL = "http://publication.pravo.gov.ru"


settings = Settings()


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        # logger.info(f"Функция {func.__name__} выполнена за {execution_time:.2f} мс")
        return result

    return wrapper


class ValidationModule:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

    @timing_decorator
    def get_documents_by_block(self, code: str) -> List[Dict]:
        url = f"{settings.EXTERNAL_URL}/api/Documents?{urlencode({'block': code, 'PageSize': 200, 'Index': 1})}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            return []

    @timing_decorator
    def get_image(self, document_id: str, page_number: int = 1) -> Image.Image:
        url = f"http://publication.pravo.gov.ru/GetImage?documentId={document_id}&pageNumber={page_number}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения {url}: {e}")
            return None

    @timing_decorator
    def extract_text_from_image(self, image: Image.Image) -> str:
        try:
            text = pytesseract.image_to_string(image, lang="rus")
            text = " ".join(text.split())
            return text.strip()
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}")
            return ""

    @timing_decorator
    def clean_text(self, text: str) -> str:
        """Очистка текста от лишних символов и приведение к нижнему регистру"""
        text = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(text.split())

    @timing_decorator
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

    @timing_decorator
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
            is_valid = similarity > 90  # Порог валидности

        # Результат
        result = {
            "original_db": db_text,
            "original_ocr": ocr_text,
            "corrected_db": db_clean,
            "similarity_percent": round(similarity, 2),
            "is_valid": is_valid,
        }
        return result

    @timing_decorator
    def process_documents(self, code: str) -> Dict:

        stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "validation_passed": 0,
            "validation_failed": 0,
            "average_similarity": 0,
            "duration": 0,
        }
        start_time = time.time()

        documents = self.get_documents_by_block(code)
        if not documents:
            logger.warning("Не удалось получить документы из API")
            return stats

        # Предполагаем, что API возвращает словарь с ключом "items"
        items = documents.get(
            "items", documents
        )  # Если "items" нет, считаем documents списком
        stats["total"] = len(items)

        total_similarity = 0
        processed = 0

        for doc in items:
            document_id = doc.get("id")
            db_text = doc.get("name", "")

            if not document_id:
                logger.warning(f"Отсутствует documentId в документе: {doc}")
                stats["failed"] += 1
                continue

            image = self.get_image(document_id)
            if image is None:
                stats["failed"] += 1
                continue

            ocr_text = self.extract_text_from_image(image)
            if not ocr_text:
                stats["failed"] += 1
                continue

            comparison = self.compare_texts(db_text, ocr_text)
            stats["successful"] += 1
            processed += 1
            total_similarity += comparison["similarity_percent"]

            # Детальное логирование для каждого документа
            logger.info(f"Документ {document_id}:")
            logger.info(f"  API текст: '{comparison['original_db']}'")
            logger.info(
                f"  OCR текст: '{comparison['original_ocr'][:200]}...'"
            )  # Ограничение длины для читаемости
            logger.info(f"  Исправленный API: '{comparison['corrected_db']}'")
            logger.info(f"  Исправленный OCR: '{comparison['corrected_db']}'")

            logger.info(f"  Схожесть: {comparison['similarity_percent']}%")
            logger.info(
                f"  Валидация: {'успешна' if comparison['is_valid'] else 'не успешна'}"
            )

            if comparison["is_valid"]:
                stats["validation_passed"] += 1
            else:
                stats["validation_failed"] += 1
                if comparison["similarity_percent"] < 90:
                    logger.warning(
                        f"  Предупреждение: низкая схожесть ({comparison['similarity_percent']}%)"
                    )

        if processed > 0:
            stats["average_similarity"] = round(total_similarity / processed, 2)

        stats["duration"] = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Итоговая статистика: {stats}")
        return stats


# Пример использования
if __name__ == "__main__":
    validator = ValidationModule()
    code = "region57"
    stats = validator.process_documents(code)
