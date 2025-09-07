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
from sqlalchemy import select, func, and_, update
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
        self.spell = SpellChecker(language="ru")

    @connection
    async def get_documents_from_db(
        self,
        session: AsyncSession,
        start_date: Union[date, datetime, str],
        end_date: Union[date, datetime, str],
    ) -> List[Dict]:
        """Получает документы из базы данных на основе фильтров"""

        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Подготовка основного запроса с дополнительными полями
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
            DocumentEntity.is_spellchek_valid,
            DocumentEntity.ocr_name,
            DocumentEntity.ocr_similarity,
        ).select_from(DocumentEntity)

        if start_date and end_date:
            query = query.filter(DocumentEntity.view_date.between(start_date, end_date))

        query = query.order_by(DocumentEntity.document_date.desc())
        result = await session.execute(query)
        documents = result.all()
        print(f"Найдено документов: {len(documents)}")
        
        # Преобразуем объекты SQLAlchemy в словари
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
                "is_spellchek_valid": doc[9],
                "ocr_name": doc[10],
                "ocr_similarity": doc[11],
            }
            docs_as_dicts.append(doc_dict)

        return docs_as_dicts

    @connection
    async def update_document_validation(
        self,
        session: AsyncSession,
        document_id: int,
        is_valid: bool,
        ocr_text: str,
        similarity: float,
        is_spellcheck_valid: bool = None,
        spellcheck_errors: str = None,
    ) -> bool:
        """Обновляет результаты валидации документа в базе данных"""
        try:
            values_dict = {
                'is_valid': is_valid,
                'ocr_name': ocr_text[:1000] if ocr_text else None,
                'ocr_similarity': similarity,
            }
            
            if is_spellcheck_valid is not None:
                values_dict['is_spellchek_valid'] = is_spellcheck_valid
            
            if spellcheck_errors is not None:
                values_dict['spellcheck_errors'] = spellcheck_errors[:2000] if spellcheck_errors else None
            
            stmt = (
                update(DocumentEntity)
                .where(DocumentEntity.id == document_id)
                .values(**values_dict)
            )
            
            await session.execute(stmt)
            await session.commit()
            
            logger.info(f"Документ {document_id} обновлен: is_valid={is_valid}, similarity={similarity}, spellcheck_valid={is_spellcheck_valid}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при обновлении документа {document_id}: {e}")
            await session.rollback()
            return False

    def check_spelling(self, text: str) -> Dict:
        """Проверяет текст на орфографические ошибки"""
        if not text or not text.strip():
            return {
                "is_valid": True,
                "errors": [],
                "error_count": 0,
                "total_words": 0,
                "corrected_text": text,
                "error_details": ""
            }
        
        cleaned_text = re.sub(r'[^\w\s\-]', ' ', text.lower())
        words = cleaned_text.split()
        
        if not words:
            return {
                "is_valid": True,
                "errors": [],
                "error_count": 0,
                "total_words": 0,
                "corrected_text": text,
                "error_details": ""
            }
        
        unknown_words = list(self.spell.unknown(words))
        errors_info = []
        corrected_words = []
        
        for word in words:
            if word in unknown_words:
                candidates = self.spell.candidates(word)
                if candidates:
                    corrected = min(candidates, key=lambda x: abs(len(x) - len(word)))
                    corrected_words.append(corrected)
                    errors_info.append({
                        "original": word,
                        "suggested": corrected,
                        "candidates": list(candidates)[:3]
                    })
                else:
                    corrected_words.append(word)
                    errors_info.append({
                        "original": word,
                        "suggested": word,
                        "candidates": []
                    })
            else:
                corrected_words.append(word)
        
        corrected_text = " ".join(corrected_words)
        
        error_details = ""
        if errors_info:
            error_details = "; ".join([
                f"{err['original']} -> {err['suggested']}" 
                for err in errors_info
            ])
        
        error_rate = len(unknown_words) / len(words) if words else 0
        is_valid = error_rate <= 0.1  # Допускаем до 10% ошибок
        
        return {
            "is_valid": is_valid,
            "errors": unknown_words,
            "error_count": len(unknown_words),
            "total_words": len(words),
            "error_rate": round(error_rate * 100, 2),
            "corrected_text": corrected_text,
            "error_details": error_details,
            "errors_info": errors_info
        }

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
                print(f"Получен ответ для документа {document_id}: {response.status_code}")
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

    def compare_texts(self, db_text: str, ocr_text: str) -> Dict:
        """Сравнение текстов с поиском названия внутри OCR-текста"""
        db_clean = self.clean_text(db_text)
        ocr_clean = self.clean_text(ocr_text)

        if db_clean in ocr_clean:
            similarity = 100.0
            is_valid = True
        else:
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
            is_valid = similarity > THRESHOLD

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
        """Обрабатывает документы из базы данных на основе указанных фильтров."""
        
        report_data = {
            "details": {},
            "summary": {
                "total": 0,
                "processed": 0,
                "skipped_already_valid": 0,
                "validation_successful": 0,
                "validation_failed": 0,
                "failed": 0,
                "updated_in_db": 0,
                "spellcheck_performed": 0,
                "spellcheck_valid": 0,
                "spellcheck_invalid": 0,
                "start_date": start_date,
                "end_date": end_date,
            },
        }

        documents = await self.get_documents_from_db(
            start_date=start_date,
            end_date=end_date,
        )

        if not documents:
            logger.warning("Не удалось получить документы из базы данных")
            if progress_callback:
                progress_callback(100, "Документы не найдены", report_data)
            return report_data

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
            
            # Определяем тексты для проверки
            name_text = doc.get("name", "").strip() if doc.get("name") else ""
            
            if doc.get("name", None):
                db_text = doc.get("name")
            elif doc.get("complex_name", None):
                db_text = doc.get("complex_name")
            elif doc.get("title", None):
                db_text = doc.get("title")
            else:
                db_text = ""

            if progress_callback:
                progress = 10 + int(80 * (idx + 1) / total_documents)
                progress_callback(
                    progress,
                    f"Обработка документа {idx+1}/{total_documents}",
                    report_data,
                )

            # Проверяем орфографию для поля name (если оно есть)
            spellcheck_result = None
            if name_text:
                spellcheck_result = self.check_spelling(name_text)
                logger.info(f"Проверка орфографии для документа {doc_id}: "
                           f"ошибок {spellcheck_result['error_count']} из {spellcheck_result['total_words']} слов, "
                           f"валидность: {spellcheck_result['is_valid']}")

            # Пропускаем уже проверенные документы
            if doc.get("is_valid") is True:
                report_data["summary"]["skipped_already_valid"] += 1
                logger.info(f"Документ {doc_id} уже проверен и валиден, пропускаем")
                
                # Но проверяем орфографию, если она еще не была проверена
                if name_text and spellcheck_result and doc.get("is_spellchek_valid") is None:
                    try:
                        update_success = await self.update_document_validation(
                            document_id=doc_id,
                            is_valid=True,
                            ocr_text=doc.get("ocr_name", "") or "",
                            similarity=doc.get("ocr_similarity", 0.0) or 0.0,
                            is_spellcheck_valid=spellcheck_result["is_valid"],
                            spellcheck_errors=spellcheck_result["error_details"]
                        )
                        if update_success:
                            report_data["summary"]["updated_in_db"] += 1
                            report_data["summary"]["spellcheck_performed"] += 1
                            if spellcheck_result["is_valid"]:
                                report_data["summary"]["spellcheck_valid"] += 1
                            else:
                                report_data["summary"]["spellcheck_invalid"] += 1
                            logger.info(f"Обновлена только орфография для документа {doc_id}")
                    except Exception as e:
                        logger.error(f"Ошибка при обновлении орфографии для документа {doc_id}: {e}")
                
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

            if not db_text.strip():
                logger.warning(f"Отсутствует текст для проверки в документе: {doc_id}")
                report_data["summary"]["failed"] += 1
                report_data["details"][doc_id] = {
                    "state": "FAILURE",
                    "error": "DATABASE", 
                    "id_reg": doc.get("id_reg"),
                    "id_type": doc.get("id_type"),
                    "reason": f"Отсутствует текст для проверки",
                }
                continue

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
            
            # Обновляем статистику проверки орфографии
            if spellcheck_result:
                report_data["summary"]["spellcheck_performed"] += 1
                if spellcheck_result["is_valid"]:
                    report_data["summary"]["spellcheck_valid"] += 1
                else:
                    report_data["summary"]["spellcheck_invalid"] += 1

            # Обновляем документ в базе данных
            update_success = await self.update_document_validation(
                document_id=doc_id,
                is_valid=comparison["is_valid"],
                ocr_text=ocr_text,
                similarity=comparison["similarity_percent"],
                is_spellcheck_valid=spellcheck_result["is_valid"] if spellcheck_result else None,
                spellcheck_errors=spellcheck_result["error_details"] if spellcheck_result else None,
            )

            if update_success:
                report_data["summary"]["updated_in_db"] += 1

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
                "updated_in_db": update_success,
                "spellcheck": spellcheck_result if spellcheck_result else None,
                "status": "success",
            }

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

        # Подсчитываем среднее значение схожести
        if processed > 0:
            report_data["summary"]["average_similarity"] = round(
                total_similarity / processed, 2
            )

        if progress_callback:
            progress_callback(
                100,
                f"Обработка завершена. Всего обработано {processed} / {total_documents} документов. "
                f"Пропущено уже проверенных: {report_data['summary']['skipped_already_valid']}",
                report_data,
            )

        logger.info(f"Итоговая статистика: %s", report_data["summary"])
        return report_data


if __name__ == "__main__":
    validator = ValidationModule()
    asyncio.run(validator.process_documents("2025-01-01", "2025-12-31", print))