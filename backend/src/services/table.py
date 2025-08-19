from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, extract, case
from sqlalchemy.orm import selectinload, joinedload
from typing import Dict, Any, List, Tuple
import math
from datetime import datetime, date

from models import DocumentEntity, TypeEntity, RegionEntity, DistrictEntity
from schemas.table import RequestTableSchema, DocumentResponseSchema, TableResponseSchema, FilterTypeEnum
from database.setup import connection


class TableService:
    
    @connection
    async def get_rows_from_table(
        self, 
        params: RequestTableSchema, 
        session: AsyncSession = None
    ) -> TableResponseSchema:
        """
        Получение документов для таблицы с учетом фильтрации и пагинации
        Логика фильтрации соответствует запросам из DashboardRepository
        """
        
        # Базовый запрос с JOIN'ами для получения связанных данных
        base_query = (
            select(DocumentEntity, TypeEntity.name, RegionEntity.name, DistrictEntity.name)
            .join(TypeEntity, DocumentEntity.id_type == TypeEntity.id)
            .join(RegionEntity, DocumentEntity.id_reg == RegionEntity.id)
            .outerjoin(DistrictEntity, RegionEntity.id_dist == DistrictEntity.id)
        )
        
        # Применяем фильтрацию
        filtered_query = self._apply_filters(base_query, params)
        
        # Подсчет общего количества записей
        count_query = select(func.count()).select_from(
            filtered_query.subquery()
        )
        total_count = await session.scalar(count_query)
        
        # Применяем сортировку
        sorted_query = self._apply_sorting(filtered_query, params)
        
        # Применяем пагинацию
        offset = (params.page - 1) * params.page_size
        paginated_query = sorted_query.offset(offset).limit(params.page_size)
        
        # Выполняем запрос
        result = await session.execute(paginated_query)
        rows = result.all()
        
        # Формируем ответ
        documents = []
        for row in rows:
            document, type_name, region_name, district_name = row
            doc_dict = {
                **{key: getattr(document, key) for key in DocumentResponseSchema.__fields__.keys() 
                   if hasattr(document, key)},
                "type_name": type_name,
                "region_name": region_name,
                "district_name": district_name
            }
            documents.append(DocumentResponseSchema(**doc_dict))
        
        total_pages = math.ceil(total_count / params.page_size) if total_count > 0 else 0
        
        return TableResponseSchema(
            documents=documents,
            total_count=total_count,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )
    
    def _apply_filters(self, query, params: RequestTableSchema):
        """
        Применение фильтров в зависимости от типа графика
        Логика основана на запросах из DashboardRepository
        """
        
        conditions = []
        
        # 1. График "Опубликование по годам" (get_publication_by_years)
        if params.type in [FilterTypeEnum.YEAR, FilterTypeEnum.YEARS]:
            year = int(params.label)
            conditions.append(extract('year', DocumentEntity.view_date) == year)
        
        # 2. График "Опубликование по типам" (get_publication_by_types)
        elif params.type in [FilterTypeEnum.TYPE, FilterTypeEnum.TYPES]:
            # Точное соответствие названию типа документа
            conditions.append(TypeEntity.name == params.label)
        
        # 3. График "Опубликование по федеральным округам" (get_publication_by_districts)
        elif params.type in [FilterTypeEnum.DISTRICT, FilterTypeEnum.DISTRICTS]:
            # Точное соответствие названию округа
            conditions.append(DistrictEntity.name == params.label)
        
        # 4. График "Опубликование по субъектам РФ" (get_publication_by_regions)
        elif params.type in [FilterTypeEnum.REGION, FilterTypeEnum.REGIONS]:
            # Проверяем, не является ли это "ОГВ Субъектов РФ"
            if params.label == "ОГВ Субъектов РФ":
                conditions.append(RegionEntity.code.like("region%"))
            else:
                conditions.append(RegionEntity.name == params.label)
        
        # 5. График "Номенклатура" - объединенный запрос (get_publication_by_nomenclature)
        # и детальный запрос (get_publication_by_nomenclature_detail_president_and_government)
        elif params.type == FilterTypeEnum.NOMENCLATURE:
            if params.label == "ОГВ Субъектов РФ":
                # Документы регионов (не president и не government)
                conditions.append(
                    and_(
                        RegionEntity.code.like("region%"),
                        ~RegionEntity.code.in_(["president", "government"])
                    )
                )
            elif params.label in [
                "Указ Президента Российской Федерации",
                "Распоряжение Президента Российской Федерации", 
                "Приказ Президента Российской Федерации"
            ]:
                # Документы президента с соответствующим типом
                conditions.append(RegionEntity.code == "president")
                if params.label == "Указ Президента Российской Федерации":
                    conditions.append(TypeEntity.name == "Указ")
                elif params.label == "Распоряжение Президента Российской Федерации":
                    conditions.append(TypeEntity.name == "Распоряжение")
                elif params.label == "Приказ Президента Российской Федерации":
                    conditions.append(TypeEntity.name == "Приказ")
            elif params.label in [
                "Постановление Правительства Российской Федерации",
                "Распоряжение Правительства Российской Федерации"
            ]:
                # Документы правительства с соответствующим типом
                conditions.append(RegionEntity.code == "government")
                if params.label == "Постановление Правительства Российской Федерации":
                    conditions.append(TypeEntity.name == "Постановление")
                elif params.label == "Распоряжение Правительства Российской Федерации":
                    conditions.append(TypeEntity.name == "Распоряжение")
            else:
                # Общий поиск по номенклатуре
                conditions.append(
                    or_(
                        TypeEntity.name.ilike(f"%{params.label}%"),
                        RegionEntity.name.ilike(f"%{params.label}%")
                    )
                )
        
        # 6. Фильтр по органу власти (для случаев когда нужно отфильтровать по signatory_authority_id)
        elif params.type == FilterTypeEnum.AUTHORITY:
            conditions.append(
                DocumentEntity.signatory_authority_id.ilike(f"%{params.label}%")
            )
        
        # Фильтрация по датам (аналогично DashboardRepository)
        # В дашборде используется view_date для фильтрации по датам
        date_filter_conditions = []
        
        if params.start_date and params.end_date:
            # Если указаны обе даты - фильтруем по диапазону
            date_filter_conditions.append(
                DocumentEntity.view_date.between(params.start_date, params.end_date)
            )
        elif params.start_date:
            # Только начальная дата
            date_filter_conditions.append(DocumentEntity.view_date >= params.start_date)
        elif params.end_date:
            # Только конечная дата
            date_filter_conditions.append(DocumentEntity.view_date <= params.end_date)
        
        if date_filter_conditions:
            conditions.extend(date_filter_conditions)
        
        # Применяем все условия
        if conditions:
            query = query.where(and_(*conditions))
        
        return query
    
    def _apply_sorting(self, query, params: RequestTableSchema):
        """Применение сортировки"""
        
        # Маппинг полей для сортировки
        sort_mapping = {
            'date_of_publication': DocumentEntity.date_of_publication,
            'date_of_signing': DocumentEntity.date_of_signing,
            'document_date': DocumentEntity.document_date,
            'view_date': DocumentEntity.view_date,
            'name': DocumentEntity.name,
            'title': DocumentEntity.title,
            'eo_number': DocumentEntity.eo_number,
            'pages_count': DocumentEntity.pages_count
        }
        
        sort_column = sort_mapping.get(params.sort_by, DocumentEntity.view_date)
        
        if params.sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())
        
        # Добавляем дополнительную сортировку по ID для стабильности результатов
        query = query.order_by(DocumentEntity.id.desc())
        
        return query