from datetime import datetime
from typing import Literal, Optional
from pydantic import ConfigDict, Field, field_validator, model_validator, validator
from .base import BaseSchema


def check_dates(start_date, end_date):
    current_date = datetime.now().strftime("%Y-%m-%d")

    if start_date is None and end_date is None:
        start_date = None
        end_date = None
    elif start_date is None and end_date is not None:
        start_date = end_date
        end_date = end_date
    elif start_date is not None and end_date is None:
        start_date = start_date
        end_date = current_date
    elif start_date is not None and end_date is not None:
        start_date = start_date
        end_date = end_date

    return start_date, end_date


class RequestSchema(BaseSchema):
    start_date: Optional[str] = Field(alias="startDate", default=None)
    end_date: Optional[str] = Field(alias="endDate", default=None)

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def convert_date(cls, value):
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
                    return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            # Если ни один формат не подошел, выбрасываем ошибку
            raise ValueError(
                f"Неверный формат даты: {value}. Ожидаются форматы: DD.MM.YYYY, YYYY-MM-DD, DD-MM-YYYY, YYYY.MM.DD."
            )
        return value

    @model_validator(mode="after")
    def adjust_dates(cls, values):
        start_date = values.start_date
        end_date = values.end_date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Логика из check_dates
        if start_date is None and end_date is None:
            values.start_date = None
            values.end_date = None
        elif start_date is None and end_date is not None:
            values.start_date = end_date
            values.end_date = end_date
        elif start_date is not None and end_date is None:
            values.start_date = start_date
            values.end_date = current_date
        elif start_date is not None and end_date is not None:
            values.start_date = start_date
            values.end_date = end_date

        # Дополнительная проверка: end_date > start_date
        if values.start_date is not None and values.end_date is not None:
            if values.end_date < values.start_date:
                raise ValueError("end_date must be greater than or equal to start_date")

        return values

    model_config = ConfigDict(
        populate_by_name=True,  # Разрешает использовать aliases для заполнения
    )


class RequestBodySchema(RequestSchema):
    ids: Optional[list[int]] = None

    @field_validator("ids", mode="before")
    @classmethod
    def parse_ids(cls, value):
        if isinstance(value, str):
            return [int(id) for id in value.split(",")]
        return value


class RequestMaxMinBodySchema(RequestSchema):
    limit: int = None
    sort: Literal["max", "min"] = "max"


class RequestRegionSchema(BaseSchema):
    districtName: Optional[str] = None
    districtId: Optional[int] = None
