from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_, Text, text, cast
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Trabajador, Area

class TrabajadorRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session


    async def add_trabajador(self, trabajador: Trabajador) -> Trabajador:
        try:
            self.session.add(trabajador)
            await self.session.commit()
            await self.session.refresh(trabajador)
            return trabajador
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al guardar el trabajador en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error inesperado en la base de datos",
                error_details=str(e)
            ) from e


    async def get_trabajadores_with_area_pagination(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(
                    Trabajador.id,
                    Trabajador.dni,
                    Trabajador.nombres,
                    Trabajador.apellido_paterno,
                    Trabajador.apellido_materno,
                    Trabajador.genero,
                    Area.nombre_area
                )
                .join(Area, Trabajador.area_id == Area.id)
                .order_by(Trabajador.id)
                .offset(offset)
                .limit(page_size)
            )
            rows = result.all()
            trabajadores_data = [dict(row._mapping) for row in rows]

            total_result = await self.session.exec(select(func.count()).select_from(Trabajador))
            total_items = total_result.first() or 0
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": trabajadores_data,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener los trabajadores de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error inesperado en la base de datos",
                error_details=str(e)
            ) from e


    async def get_all_id_and_name(self) -> List[Dict[str, Any]]:
        try:
            query = text("SELECT fn_trabajadores_listar()")
            async with self.session.connection() as connection:
                result = await connection.execute(query)
                res = result.scalar()
            return res if res else []
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener la lista de trabajadores de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException("Ocurrio un error inesperado en la base de datos", error_details=str(e)) from e


    async def update_trabajador(self, trabajador: Trabajador) -> Trabajador:
        try:
            self.session.add(trabajador)
            await self.session.commit()
            await self.session.refresh(trabajador)
            return trabajador
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar el trabajador en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException("Error inesperado en la base de datos", error_details=str(e)) from e


    async def delete_by_id(self, trabajador_id: int) -> None:
        try:
            trabajador = await self.session.get(Trabajador, trabajador_id)
            if trabajador:
                await self.session.delete(trabajador)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al eliminar el trabajador de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException("Error inesperado en la base de datos", error_details=str(e)) from e


    async def get_by_id(self, trabajador_id: int) -> Optional[Trabajador]:
        try:
            trabajador = await self.session.get(Trabajador, trabajador_id)
            return trabajador
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el trabajador de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException("Error inesperado en la base de datos", error_details=str(e)) from e


    async def exists_trabajador_by_dni(self, dni: int) -> bool:
        try:
            result = await self.session.exec(select(Trabajador).where(Trabajador.dni == dni))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al verificar la existencia del trabajador en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error inesperado en la base de datos",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Dict[str, Any]]:
        try:
            search_filter = or_(
                cast(Trabajador.dni, Text).contains(search_string),
                Trabajador.nombres.contains(search_string),
                Trabajador.apellido_paterno.contains(search_string),
                Trabajador.apellido_materno.contains(search_string)
            )
            result = await self.session.exec(
                select(
                    Trabajador.id,
                    Trabajador.dni,
                    Trabajador.nombres,
                    Trabajador.apellido_paterno,
                    Trabajador.apellido_materno,
                    Trabajador.genero,
                    Area.nombre_area
                )
                .join(Area, Trabajador.area_id == Area.id)
                .where(search_filter)
            )
            rows = result.all()
            trabajadores_data = [dict(row._mapping) for row in rows]
            return trabajadores_data
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al buscar el trabajador en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error inesperado en la base de datos",
                error_details=str(e)
            ) from e
