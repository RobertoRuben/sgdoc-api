from typing import Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session

class ComunicacionAreaRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            query = text("""
                SELECT fn_comunicacion_areas_listar_paginado(:page, :page_size)
            """)
            async with self.session.connection() as connection:
                result = await connection.execute(query, {"page": page, "page_size": page_size})
                paginated_result = result.scalar()
            if paginated_result:
                return paginated_result
            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener la lista comunicaciones entre áreas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener la lista comunicaciones entre áreas",
                error_details=str(e)
            ) from e


    async def get_areas_destino_by_area_origen_id(self, area_origen_id: int) -> List[Dict[str, Any]]:
        try:
            query = text("""
                SELECT fn_comunicaciones_areas_obtener_area_destino_por_area_origen_id(:area_origen_id)
            """)
            async with self.session.connection() as connection:
                result = await connection.execute(query, {"area_origen_id": area_origen_id})
                areas = result.scalar()
            return areas if areas else []
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener las áreas destino por área origen ID",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener las áreas destino por área origen ID",
                error_details=str(e)
            ) from e
