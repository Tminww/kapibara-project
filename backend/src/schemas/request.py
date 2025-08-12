from datetime import datetime
from typing import Annotated, Literal, Optional
from fastapi import Query
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
        populate_by_name=True,
        validate_assignment=False,
    )


class RequestValidatorStartSchema(RequestSchema):
    send_email: Optional[bool] = Field(alias="sendEmail", default=False)
    recipient_email: Optional[str] = Field(
        alias="recipientEmail", default="example@example.com"
    )


class RequestBodySchema(RequestSchema):
    ids: Optional[str] = None

    @field_validator("ids", mode="after")
    @classmethod
    def check_ids(cls, value):
        if value is None:
            return None
        return [int(id.strip()) for id in value.split(",")]


class RequestMaxMinBodySchema(RequestSchema):
    limit: int = Query(gt=0, le=100, default=10)
    sort: Literal["max", "min"] = "max"


class RequestRegionSchema(BaseSchema):
    districtName: Optional[str] = None
    districtId: Optional[int] = None

    @model_validator(mode="after")
    def check_params(cls, values):
        if not values:
            return

        if values.districtId and values.districtName:
            raise ValueError("districtName or districtId must be provided")

        return values


class RequestNomenclatureSchema(RequestSchema):
    detail: Optional[bool] = False

class RequestTableSchema(RequestSchema):
    type: Optional[str]
    label: Optional[str]