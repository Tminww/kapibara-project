from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class FilterTypeEnum(str, Enum):
    """Типы фильтрации для разных графиков дашборда"""
    
    # График "Опубликование по годам" 
    YEAR = "year"
    YEARS = "years"
    
    # График "Опубликование по типам документов"
    TYPE = "type"
    TYPES = "types"
    
    # График "Опубликование по федеральным округам"
    DISTRICT = "district"
    DISTRICTS = "districts"
    
    # График "Опубликование по субъектам РФ (топ-10)"
    REGION = "region"
    REGIONS = "regions"
    
    # График "Номенклатура" (общий и детальный для президента/правительства)
    NOMENCLATURE = "nomenclature"
    
    # Дополнительные фильтры
    AUTHORITY = "authority"  # Фильтр по органу власти


class RequestTableSchema(BaseModel):
    """Схема запроса для получения таблицы документов"""
    
    # Основные параметры фильтрации
    type: FilterTypeEnum = Field(..., description="Тип фильтра")
    label: str = Field(..., description="Значение для поиска")
    
    # Даты для дополнительной фильтрации (используется view_date как в дашборде)
    start_date: Optional[date] = Field(None, alias="startDate", description="Начальная дата")
    end_date: Optional[date] = Field(None, alias="endDate", description="Конечная дата")
    
    # Пагинация
    page: int = Field(1, ge=1, description="Номер страницы")
    page_size: int = Field(20, ge=1, le=100, description="Размер страницы")
    
    # Сортировка
    sort_by: str = Field("view_date", description="Поле для сортировки")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Направление сортировки")

    class Config:
        populate_by_name = True


class DocumentResponseSchema(BaseModel):
    """Схема ответа для одного документа"""
    id: int
    eo_number: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    complex_name: Optional[str] = None
    document_date: Optional[date] = None
    date_of_publication: Optional[date] = None
    date_of_signing: Optional[date] = None
    view_date: Optional[date] = None
    pages_count: Optional[int] = None
    signatory_authority_id: Optional[str] = None
    number: Optional[str] = None
    external_id: Optional[str] = None
    
    # Связанные данные
    type_name: Optional[str] = None
    region_name: Optional[str] = None
    district_name: Optional[str] = None

    class Config:
        from_attributes = True


class TableResponseSchema(BaseModel):
    """Схема ответа для таблицы документов"""
    documents: List[DocumentResponseSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ResponseSchema(BaseModel):
    """Общая схема ответа"""
    data: TableResponseSchema
    message: str = "Success"
    status: int = 200


# Дополнительные схемы для маппинга типов графиков
class ChartTypeMapping:
    """Маппинг типов графиков к FilterTypeEnum"""
    
    CHART_MAPPINGS = {
        # 1. График "Опубликование по номенклатуре" (get_publication_by_nomenclature)
        "nomenclature_general": FilterTypeEnum.NOMENCLATURE,
        
        # 2. График "Опубликование по годам" (get_publication_by_years)  
        "by_years": FilterTypeEnum.YEARS,
        
        # 3. График "Опубликование по федеральным округам" (get_publication_by_districts)
        "by_districts": FilterTypeEnum.DISTRICTS,
        
        # 4. График "Топ-10/Топ-N субъектов РФ" (get_publication_by_regions)
        "by_regions": FilterTypeEnum.REGIONS,
        
        # 5. График "Детальная номенклатура президента и правительства" (get_publication_by_nomenclature_detail_president_and_government)
        "nomenclature_detail": FilterTypeEnum.NOMENCLATURE,
        
        # 6. График "Опубликование по типам" (get_publication_by_types)
        "by_types": FilterTypeEnum.TYPES,
    }

    @classmethod
    def get_filter_type(cls, chart_type: str) -> FilterTypeEnum:
        """Получить FilterTypeEnum по типу графика"""
        return cls.CHART_MAPPINGS.get(chart_type, FilterTypeEnum.NOMENCLATURE)


# Примеры значений label для каждого типа графика
class LabelExamples:
    """Примеры значений label для разных типов фильтрации"""
    
    EXAMPLES = {
        FilterTypeEnum.YEAR: ["2024", "2023", "2022"],
        FilterTypeEnum.YEARS: ["2024", "2023", "2022"],
        
        FilterTypeEnum.TYPE: [
            "Закон", "Постановление", "Распоряжение", "Указ", "Приказ"
        ],
        FilterTypeEnum.TYPES: [
            "Закон", "Постановление", "Распоряжение", "Указ", "Приказ"
        ],
        
        FilterTypeEnum.DISTRICT: [
            "Центральный федеральный округ",
            "Северо-Западный федеральный округ", 
            "Южный федеральный округ",
            "Северо-Кавказский федеральный округ",
            "Приволжский федеральный округ",
            "Уральский федеральный округ",
            "Сибирский федеральный округ",
            "Дальневосточный федеральный округ"
        ],
        FilterTypeEnum.DISTRICTS: [
            "Центральный федеральный округ",
            "Северо-Западный федеральный округ", 
            "Южный федеральный округ"
        ],
        
        FilterTypeEnum.REGION: [
            "Красноярский край", "Москва", "Санкт-Петербург",
            "Московская область", "ОГВ Субъектов РФ"
        ],
        FilterTypeEnum.REGIONS: [
            "Красноярский край", "Москва", "Санкт-Петербург",
            "ОГВ Субъектов РФ"
        ],
        
        FilterTypeEnum.NOMENCLATURE: [
            "ОГВ Субъектов РФ",
            "Указ Президента Российской Федерации",
            "Распоряжение Президента Российской Федерации",
            "Приказ Президента Российской Федерации",
            "Постановление Правительства Российской Федерации",
            "Распоряжение Правительства Российской Федерации"
        ],
        
        FilterTypeEnum.AUTHORITY: [
            "Правительство", "Президент", "Министерство"
        ]
    }