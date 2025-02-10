from typing import List, Dict, Any, Optional
from fastapi import Depends
from sqlmodel import select, or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity.area import Area


class AreaRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_area(self, area: Area) -> Area:
        try:
            self.session.add(area)
            await self.session.commit()
            await self.session.refresh(area)
            return area
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al agregar el área",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al agregar el área",
                error_details=str(e)
            ) from e


    async def get_all_areas(self) -> List[Area]:
        try:
            result = await self.session.exec(select(Area))
            areas = result.all()
            return list(areas)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener las áreas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener las áreas",
                error_details=str(e)
            ) from e


    async def update_area(self, area: Area) -> Area:
        try:
            self.session.add(area)
            await self.session.commit()
            await self.session.refresh(area)
            return area
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al actualizar el área",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al actualizar el área",
                error_details=str(e)
            ) from e


    async def delete_area_by_id(self, area_id: int) -> None:
        try:
            area = await self.session.get(Area, area_id)
            if area:
                await self.session.delete(area)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al eliminar el área",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al eliminar el área",
                error_details=str(e)
            ) from e


    async def get_area_by_id(self, area_id: int) -> Optional[Area]:
        try:
            area = await self.session.get(Area, area_id)
            return area
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener el área por ID",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener el área por ID",
                error_details=str(e)
            ) from e


    async def exists(self, nombre_area: str) -> bool:
        try:
            result = await self.session.exec(
                select(Area).where(Area.nombre_area == nombre_area)
            )
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia del área",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia del área",
                error_details=str(e)
            ) from e


    async def exists_by_id(self, area_id: int) -> bool:
        try:
            area = await self.session.get(Area, area_id)
            return area is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia del área por ID",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia del área por ID",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Area]:
        try:
            search_filter = or_(Area.nombre_area.contains(search_string))
            result = await self.session.exec(select(Area).where(search_filter))
            areas = result.all()
            return list(areas)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al buscar áreas por cadena",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al buscar áreas por cadena",
                error_details=str(e)
            ) from e


    async def get_all_pagination(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            offset = (page - 1) * page_size
            result = await self.session.exec(
                select(Area)
                .order_by(Area.id)
                .offset(offset)
                .limit(page_size)
            )
            areas = result.all()

            count_result = await self.session.exec(
                select(func.count()).select_from(Area)
            )
            total_items = count_result.first()
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": areas,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener las áreas paginadas",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener las áreas paginadas",
                error_details=str(e)
            ) from e
