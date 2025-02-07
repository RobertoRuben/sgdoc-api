from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_, Text, cast
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database import get_async_session
from fastapi import Depends
from src.exception import DatabaseException
from src.model.entity import Rol


class RolRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session


    async def add_rol(self, rol: Rol) -> Rol:
        try:
            self.session.add(rol)
            await self.session.commit()
            await self.session.refresh(rol)
            return rol
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al guardar el rol en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[Rol]:
        try:
            result = await self.session.exec(select(Rol))
            roles = result.all()
            return list(roles)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener los roles de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def update_rol(self, rol: Rol) -> Rol:
        try:
            self.session.add(rol)
            await self.session.commit()
            await self.session.refresh(rol)
            return rol
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar el rol en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, rol_id: int) -> None:
        try:
            rol = await self.session.get(Rol, rol_id)
            if rol:
                await self.session.delete(rol)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al eliminar el rol de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def get_by_id(self, rol_id: int) -> Optional[Rol]:
        try:
            rol = await self.session.get(Rol, rol_id)
            return rol
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el rol de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def exists(self, nombre_rol: str) -> bool:
        try:
            result = await self.session.exec(select(Rol).where(Rol.nombre_rol == nombre_rol))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar si existe el rol en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Rol]:
        try:
            search_filter = or_(
                Rol.nombre_rol.contains(search_string),
                cast(Rol.id, Text).contains(search_string)
            )
            result = await self.session.exec(select(Rol).where(search_filter))
            roles = result.all()
            return roles
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al buscar los roles en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e


    async def get_all_pagination(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(Rol)
                .order_by(Rol.id)
                .offset(offset)
                .limit(page_size)
            )
            roles = result.all()
            total_result = await self.session.exec(select(func.count()).select_from(Rol))
            total_items = total_result.first() or 0
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": roles,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener los roles de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error inesperado",
                error_details=str(e)
            ) from e
