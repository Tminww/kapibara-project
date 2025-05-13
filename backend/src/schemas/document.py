from datetime import datetime
from typing import Optional

from pydantic import field_validator

from .base import BaseSchema
from utils import parser_logger as logger


class DocumentSchema(BaseSchema):
    eo_number: Optional[str] = None
    complex_name: Optional[str] = None
    pages_count: Optional[int] = None
    pdf_file_length: Optional[int] = None
    name: Optional[str] = None
    signatory_authority_id: Optional[str] = None
    number: Optional[str] = None
    document_date: Optional[datetime] = None
    view_date: Optional[datetime] = None
    title: Optional[str] = None
    external_id: Optional[str] = None
    id_type: int
    id_reg: int
    hash: Optional[str] = None
    date_of_publication: Optional[datetime] = None
    date_of_signing: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator(
        "complex_name",
        "name",
        "title",
        mode="before",
    )
    @classmethod
    def clean_text(cls, value):
        """Убирает переносы строк и лишние пробелы из строковых полей."""
        if value is None:
            return None
        value = value.replace("<br />", " ").replace("<br>", " ")
        return " ".join(str(value).split())

    @field_validator(
        "document_date",
        "view_date",
        "date_of_publication",
        "date_of_signing",
        "updated_at",
        mode="before",
    )
    @classmethod
    def str_to_date(cls, value):
        if isinstance(value, str):
            # Список поддерживаемых форматов
            date_formats = [
                "%d.%m.%Y",  # dd.mm.yyyy (например, 17.03.2025)
                "%Y-%m-%d",  # yyyy-mm-dd (например, 2025-03-17)
                "%d-%m-%Y",  # dd-mm-yyyy (например, 17-03-2025)
                "%Y.%m.%d",  # yyyy.mm.dd (например, 2025.03.17)
            ]
            for fmt in date_formats:
                try:
                    # Парсим строку и возвращаем объект datetime
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            logger.error(
                "Неверный формат даты: {value}. Ожидаются форматы: DD.MM.YYYY, YYYY-MM-DD, DD-MM-YYYY, YYYY.MM.DD."
            )
            # Если ни один формат не подошел, выбрасываем ошибку
            raise ValueError(
                f"Неверный формат даты: {value}. Ожидаются форматы: DD.MM.YYYY, YYYY-MM-DD, DD-MM-YYYY, YYYY.MM.DD."
            )
        return value


class DocumentSelectSchema(DocumentSchema):
    id: int
