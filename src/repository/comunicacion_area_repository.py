from typing import Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlmodel import text, select, and_, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import ComunicacionArea, Area

class ComunicacionAreaRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get_all_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            query = text("""
                SELECT fn_comunicacion_areas_listar_paginado(:page, :page_size)
            """)
            result = await self.session.execute(query, {"page": page, "page_size": page_size})
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
            result = await self.session.execute(query, {"area_origen_id": area_origen_id})
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


    async def add_comunicacion(self, comunicacion_area: ComunicacionArea) -> ComunicacionArea:
        try:
            self.session.add(comunicacion_area)
            await self.session.commit()
            await self.session.refresh(comunicacion_area)
            return comunicacion_area
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al agregar la comunicación entre áreas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al agregar la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def update_comunicacion(self, comunicacion_area: ComunicacionArea) -> ComunicacionArea:
        try:
            await self.session.commit()
            await self.session.refresh(comunicacion_area)
            return comunicacion_area
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al actualizar la comunicación entre áreas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al actualizar la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def get_by_id(self, comunicacion_area_id: int) -> ComunicacionArea:
        try:
            comunicacion_area = await self.session.get(ComunicacionArea, comunicacion_area_id)
            return comunicacion_area
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener la comunicación entre áreas por ID",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener la comunicación entre áreas por ID",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, comunicacion_area_id: int) -> None:
        try:
            comunicacion_area = await self.session.get(ComunicacionArea, comunicacion_area_id)
            if comunicacion_area:
                await self.session.delete(comunicacion_area)
                await self.session.commit()
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al eliminar la comunicación entre áreas por ID",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al eliminar la comunicación entre áreas por ID",
                error_details=str(e)
            ) from e


    async def exists(self, area_origen_id: int, area_destino_id: int) -> bool:
        try:
            result = await self.session.exec(
                select(ComunicacionArea).where(
                    and_(
                        ComunicacionArea.area_origen_id == area_origen_id,
                        ComunicacionArea.area_destino_id == area_destino_id
                    )
                )
            )
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia de la comunicación entre áreas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia de la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def find_by_area_nombre(self, search_string: str) -> List[Dict[str, Any]]:
        try:
            area_origen = aliased(Area, name="area_origen")
            area_destino = aliased(Area, name="area_destino")

            stmt = (
                select(
                ComunicacionArea.id,
                    ComunicacionArea.area_origen_id,
                    ComunicacionArea.area_destino_id,
                    area_origen.nombre_area.label("area_origen_nombre"),
                    area_destino.nombre_area.label("area_destino_nombre")
                )
                .join(area_origen, ComunicacionArea.area_origen_id == area_origen.id)
                .join(area_destino, ComunicacionArea.area_destino_id == area_destino.id)
                .where(
                    or_(
                        area_origen.nombre_area.contains(search_string),
                        area_destino.nombre_area.contains(search_string)
                    )
                )
            )
            result = await self.session.exec(stmt)
            comunicaciones = result.mappings().all()
            return list(comunicaciones)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al buscar comunicaciones por nombre de área",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al buscar comunicaciones por nombre de área",
                error_details=str(e)
            ) from e
