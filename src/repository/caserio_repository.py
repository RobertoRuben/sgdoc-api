from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Caserio, CentroPoblado

class CaserioRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_caserio(self, caserio: Caserio) -> Caserio:
        try:
            self.session.add(caserio)
            await self.session.commit()
            await self.session.refresh(caserio)
            return caserio
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al registrar el caserio",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al registrar el caserio",
                error_details=str(e)
            ) from e


    async def get_caserios_names(self) -> List[Caserio]:
        try:
            result = await self.session.exec(
                select(Caserio.id, Caserio.nombre_caserio)
                .where(Caserio.centro_poblado_id == None)
            )
            caserios = result.all()
            return caserios
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener la lista de nombres de los caserios",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista de nombres de los caserios",
                error_details=str(e)
            ) from e


    async def update_caserio(self, caserio: Caserio) -> Caserio:
        try:
            self.session.add(caserio)
            await self.session.commit()
            await self.session.refresh(caserio)
            return caserio
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al actualizar el caserio",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al actualizar el caserio",
                error_details=str(e)
            ) from e


    async def delete_caserio_by_id(self, caserio_id: int) -> None:
        try:
            caserio = await self.session.get(Caserio, caserio_id)
            if caserio:
                await self.session.delete(caserio)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al eliminar el caserio",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al eliminar el caserio",
                error_details=str(e)
            ) from e


    async def get_caserio_by_id(self, caserio_id: int) -> Optional[Caserio]:
        try:
            caserio = await self.session.get(Caserio, caserio_id)
            return caserio
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener el caserio",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener el caserio",
                error_details=str(e)
            ) from e


    async def exists(self, nombre_caserio: str) -> bool:
        try:
            result = await self.session.exec(
                select(Caserio).where(Caserio.nombre_caserio == nombre_caserio)
            )
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al verificar la existencia del caserio",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al verificar la existencia del caserio",
                error_details=str(e)
            ) from e


    async def get_all_caserios_by_centro_poblado_id(self, centro_poblado_id: Optional[int]) -> List[Caserio]:
        try:
            if centro_poblado_id is not None:
                result = await self.session.exec(
                    select(Caserio).where(Caserio.centro_poblado_id == centro_poblado_id)
                )
            else:
                result = await self.session.exec(select(Caserio))
            caserios = result.all()
            return list(caserios)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener los caserios por ID de centro poblado",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener los caserios por ID de centro poblado",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Dict[str, Any]]:
        try:
            search_filter = or_(Caserio.nombre_caserio.contains(search_string))
            result = await self.session.exec(
                select(
                    Caserio.id,
                    Caserio.nombre_caserio,
                    CentroPoblado.nombre_centro_poblado
                )
                .join(CentroPoblado, Caserio.centro_poblado_id == CentroPoblado.id, isouter=True)
                .where(search_filter)
            )
            rows = result.all()
            caserios_data = [dict(row._mapping) for row in rows]
            return list(caserios_data)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al buscar los caseríos por nombre",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al buscar los caseríos por nombre",
                error_details=str(e)
            ) from e


    async def get_all_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(
                    Caserio.id,
                    Caserio.nombre_caserio,
                    CentroPoblado.nombre_centro_poblado
                )
                .join(CentroPoblado, Caserio.centro_poblado_id == CentroPoblado.id, isouter=True)
                .order_by(Caserio.id)
                .offset(offset)
                .limit(page_size)
            )
            rows = result.all()
            caserios_data = [dict(row._mapping) for row in rows]
            count_result = await self.session.exec(
                select(func.count()).select_from(Caserio)
            )
            total_items = count_result.first()
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": caserios_data,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener la lista de caserios paginada",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener la lista de caserios paginada",
                error_details=str(e)
            ) from e
