from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import CentroPoblado

class CentroPobladoRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_centro_poblado(self, centro_poblado: CentroPoblado) -> CentroPoblado:
        try:
            self.session.add(centro_poblado)
            await self.session.commit()
            await self.session.refresh(centro_poblado)
            return centro_poblado
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al guardar el centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al guardar el centro poblado",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[CentroPoblado]:
        try:
            result = await self.session.exec(select(CentroPoblado))
            centro_poblados = result.all()
            return list(centro_poblados)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener la lista de centros poblados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista de centros poblados",
                error_details=str(e)
            ) from e


    async def update_centro_poblado(self, centro_poblado: CentroPoblado) -> CentroPoblado:
        try:
            self.session.add(centro_poblado)
            await self.session.commit()
            await self.session.refresh(centro_poblado)
            return centro_poblado
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al actualizar el centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al actualizar el centro poblado",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, centro_poblado_id: int) -> None:
        try:
            centro_poblado = await self.session.get(CentroPoblado, centro_poblado_id)
            if centro_poblado:
                await self.session.delete(centro_poblado)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al eliminar el centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al eliminar el centro poblado",
                error_details=str(e)
            ) from e


    async def get_by_id(self, centro_poblado_id: int) -> Optional[CentroPoblado]:
        try:
            centro_poblado = await self.session.get(CentroPoblado, centro_poblado_id)
            return centro_poblado
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener el centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener el centro poblado",
                error_details=str(e)
            ) from e


    async def exist(self, nombre_centro_poblado: str) -> bool:
        try:
            result = await self.session.exec(
                select(CentroPoblado).where(CentroPoblado.nombre_centro_poblado == nombre_centro_poblado)
            )
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia del centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia del centro poblado",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[CentroPoblado]:
        try:
            search_filter = or_(
                CentroPoblado.nombre_centro_poblado.contains(search_string)
            )
            result = await self.session.exec(
                select(CentroPoblado).where(search_filter)
            )
            centro_poblados = result.all()
            return list(centro_poblados)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al buscar el centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al buscar el centro poblado",
                error_details=str(e)
            ) from e


    async def get_all_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(CentroPoblado)
                .order_by(CentroPoblado.id)
                .offset(offset)
                .limit(page_size)
            )
            centro_poblados = result.all()

            count_result = await self.session.exec(
                select(func.count()).select_from(CentroPoblado)
            )
            total_items = count_result.first()
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": centro_poblados,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener la lista paginada de centros poblados",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista paginada de centros poblados",
                error_details=str(e)
            ) from e
