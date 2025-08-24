from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from services import TableService as Service
from schemas.table import RequestTableSchema, ResponseSchema, FilterTypeEnum
from .dependencies import get_table_service as get_service

router = APIRouter(prefix="/table", tags=["table"])

@router.get("", response_model=ResponseSchema)
async def get_table(
    service: Annotated[Service, Depends(get_service)],
    
    # Основные параметры фильтрации
    type: FilterTypeEnum = Query(..., description="Тип фильтра для документов"),
    label: str = Query(..., description="Значение для поиска (тип документа для новых фильтров)"),
    
    # Новый параметр для названия округа/региона
    name: str = Query(None, description="Название федерального округа или региона"),
    
    # Даты (опциональные) - используется view_date как в дашборде
    startDate: str = Query(None, description="Начальная дата в формате DD.MM.YYYY"),
    endDate: str = Query(None, description="Конечная дата в формате DD.MM.YYYY"),
    
    # Пагинация
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    
    # Сортировка
    sort_by: str = Query("view_date", description="Поле для сортировки"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Направление сортировки"),
    
) -> ResponseSchema:
    """
    Получение таблицы документов с фильтрацией по данным из графиков дашборда
    
    ## Соответствие графиков дашборда и параметров:
    
    ### 1. График "Опубликование по номенклатуре":
    ```
    /table?type=nomenclature&label=ОГВ Субъектов РФ
    /table?type=nomenclature&label=Указ Президента Российской Федерации
    /table?type=nomenclature&label=Постановление Правительства Российской Федерации
    ```
    
    ### 2. График "Опубликование по годам":
    ```
    /table?type=years&label=2024
    /table?type=years&label=2023
    ```
    
    ### 3. График "Опубликование по федеральным округам":
    ```
    /table?type=districts&label=Сибирский федеральный округ
    /table?type=districts&label=Центральный федеральный округ
    ```
    
    ### 4. График "Топ-10 субъектов РФ":
    ```
    /table?type=regions&label=Красноярский край
    /table?type=regions&label=ОГВ Субъектов РФ
    ```
    
    ### 5. График "Опубликование по типам документов":
    ```
    /table?type=types&label=Закон
    /table?type=types&label=Постановление
    ```
    
    ### 6. НОВЫЕ типы фильтров:
    
    #### 6.1. Конкретный тип документа в федеральном округе:
    ```
    /table?type=district-type&label=Постановление&name=Северо-Кавказский ФО
    /table?type=district-type&label=Указ&name=Центральный федеральный округ
    ```
    
    #### 6.2. Конкретный тип документа в регионе:
    ```
    /table?type=region-type&label=Закон&name=Красноярский край
    /table?type=region-type&label=Постановление&name=Москва
    ```
    
    #### 6.3. Конкретный тип документа во всех регионах:
    ```
    /table?type=districts-type-all&label=Постановление
    /table?type=districts-type-all&label=Закон
=======
    ### 6. Детальная номенклатура президента и правительства:
    ```
    /table?type=nomenclature&label=Указ Президента Российской Федерации
    /table?type=nomenclature&label=Распоряжение Правительства Российской Федерации
>>>>>>> a6fcbac (add: Сделал страницу с таблицей для всех графиков со страницы Dashboard)
    ```
    
    ### 7. С дополнительной фильтрацией по датам:
    ```
    /table?type=district-type&label=Постановление&name=Северо-Кавказский ФО&startDate=01.07.2025&endDate=31.07.2025
    /table?type=region-type&label=Закон&name=Красноярский край&startDate=01.01.2024&endDate=31.12.2024
    /table?type=districts-type-all&label=Постановление&startDate=01.06.2025&endDate=30.06.2025
    /table?type=nomenclature&label=ОГВ Субъектов РФ&startDate=01.07.2025&endDate=31.07.2025
    /table?type=districts&label=Сибирский федеральный округ&startDate=01.01.2024&endDate=31.12.2024
    ```
    
    ## Примечания:
    - Фильтрация по датам использует поле `view_date` (как в дашборде)

    - Поддержка детальной номенклатуры для документов президента и правительства
    """
    
    try:
        # Преобразуем строковые параметры в объект RequestTableSchema
        params_dict = {
            "type": type,
            "label": label,
            "name": name,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
        
        # Парсим даты если они переданы
        if startDate:
            try:
                params_dict["start_date"] = datetime.strptime(startDate, "%d.%m.%Y").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Неверный формат начальной даты: {startDate}. Используйте DD.MM.YYYY"
                )
        
        if endDate:
            try:
                params_dict["end_date"] = datetime.strptime(endDate, "%d.%m.%Y").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Неверный формат конечной даты: {endDate}. Используйте DD.MM.YYYY"
                )
        
        # Валидация sort_by
        allowed_sort_fields = [
            "view_date", "date_of_publication", "date_of_signing", "document_date",
            "name", "title", "eo_number", "pages_count"
        ]
        if sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимое поле для сортировки: {sort_by}. Доступные поля: {allowed_sort_fields}"
            )
        
        # Валидация новых типов фильтров
        if type in [FilterTypeEnum.DISTRICT_TYPE, FilterTypeEnum.REGION_TYPE] and not name:
            raise HTTPException(
                status_code=400,
                detail=f"Для типа фильтра '{type}' параметр 'name' является обязательным"
            )
        
        params = RequestTableSchema(**params_dict)
        response = await service.get_rows_from_table(params)
        
        return ResponseSchema(data=response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.get("/filters")
async def get_available_filters() -> dict:
    """
    Получение доступных типов фильтров и их описания
    """
    return {
        "filter_types": {
            "year": {
                "name": "Год",
                "description": "Фильтрация по году публикации документа",
                "example": "2024",
                "requires_name": False
            },
            "years": {
                "name": "Года", 
                "description": "Фильтрация по году публикации документа (альтернативный вариант)",
                "example": "2024",
                "requires_name": False
            },
            "type": {
                "name": "Тип документа", 
                "description": "Фильтрация по типу нормативно-правового акта",
                "example": "Закон о внесении поправок в Устав Красноярского края",
                "requires_name": False
            },
            "types": {
                "name": "Типы документов",
                "description": "Фильтрация по типам нормативно-правовых актов (альтернативный вариант)",
                "example": "Закон о внесении поправок в Устав Красноярского края",
                "requires_name": False
            },
            "district": {
                "name": "Федеральный округ",
                "description": "Фильтрация по федеральному округу",
                "example": "Сибирский федеральный округ",
                "requires_name": False
            },
            "region": {
                "name": "Субъект РФ",
                "description": "Фильтрация по региону/субъекту Российской Федерации",
                "example": "Красноярский край",
                "requires_name": False
            },
            "nomenclature": {
                "name": "Номенклатура",
                "description": "Поиск в названии, заголовке или полном наименовании документа",
                "example": "Постановление",
                "requires_name": False
            },
            "authority": {
                "name": "Орган власти",
                "description": "Фильтрация по подписывающему органу власти",
                "example": "Правительство",
                "requires_name": False
            },
            "district-type": {
                "name": "Тип документа в федеральном округе",
                "description": "Фильтрация по конкретному типу документа в определенном федеральном округе",
                "example": "label=Постановление&name=Северо-Кавказский ФО",
                "requires_name": True
            },
            "region-type": {
                "name": "Тип документа в регионе",
                "description": "Фильтрация по конкретному типу документа в определенном регионе",
                "example": "label=Закон&name=Красноярский край",
                "requires_name": True
            },
            "districts-type-all": {
                "name": "Тип документа во всех регионах",
                "description": "Фильтрация по конкретному типу документа во всех региональных документах",
                "example": "label=Постановление",
                "requires_name": False
            }
        },
        "sort_fields": [
            "date_of_publication",
            "date_of_signing", 
            "document_date",
            "view_date",
            "name",
            "title",
            "eo_number",
            "pages_count"
        ],
        "examples": {
            "district_type": "/table?type=district-type&label=Постановление&name=Северо-Кавказский ФО&startDate=01.07.2025&endDate=31.07.2025",
            "region_type": "/table?type=region-type&label=Закон&name=Красноярский край",
            "districts_type_all": "/table?type=districts-type-all&label=Постановление"
        }
    }