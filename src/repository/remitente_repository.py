from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func, or_, Text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Remitente

class RemitenteRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session


    async def add_remitentes(self, remitente: Remitente) -> Remitente:
        try:
            self.session.add(remitente)
            await self.session.commit()
            await self.session.refresh(remitente)
            return remitente
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al registrar el remitente en la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al registrar el remitente en la base",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[Remitente]:
        try:
            result = await self.session.exec(select(Remitente))
            remitentes = result.all()
            return list(remitentes)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener los remitentes de la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener los remitentes de la base",
                error_details=str(e)
            ) from e


    async def update_remitente(self, remitente: Remitente) -> Remitente:
        try:
            self.session.add(remitente)
            await self.session.commit()
            await self.session.refresh(remitente)
            return remitente
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al actualizar el remitente en la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al actualizar el remitente en la base",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, remitente_id: int) -> None:
        try:
            remitente = await self.session.get(Remitente, remitente_id)
            if remitente:
                await self.session.delete(remitente)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error al eliminar el remitente de la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Ocurrio un error desconocido al eliminar el remitente de la base",
                error_details=str(e)
            ) from e


    async def get_by_id(self, remitente_id: int) -> Optional[Remitente]:
        try:
            remitente = await self.session.get(Remitente, remitente_id)
            return remitente
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener el remitente",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener el remitente",
                error_details=str(e)
            ) from e


    async def exists(self, dni: int) -> bool:
        try:
            result = await self.session.exec(select(Remitente).where(Remitente.dni == dni))
            return result.first() is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al verificar la existencia del remitente en la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al verificar la existencia del remitente en la base",
                error_details=str(e)
            ) from e


    async def find_by_string(self, search_string: str) -> List[Remitente]:
        try:
            search_filter = or_(
                Remitente.nombres.contains(search_string),
                Remitente.apellido_paterno.contains(search_string),
                func.cast(Remitente.dni, Text).contains(search_string)
            )
            result = await self.session.exec(select(Remitente).where(search_filter))
            remitentes = result.all()
            return list(remitentes)
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al buscar los remitentes en la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al buscar los remitentes en la base",
                error_details=str(e)
            ) from e


    async def get_all_pagination(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(Remitente)
                .order_by(Remitente.id)
                .offset(offset)
                .limit(page_size)
            )
            remitentes = result.all()
            total_result = await self.session.exec(select(func.count()).select_from(Remitente))
            total_items = total_result.first() or 0
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": remitentes,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener los remitentes de la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener los remitentes de la base",
                error_details=str(e)
            ) from e


    async def get_by_dni(self, dni: int) -> Optional[Remitente]:
        try:
            result = await self.session.exec(select(Remitente).where(Remitente.dni == dni))
            remitente = result.first()
            return remitente
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Ocurrio un error al obtener el remitente de la base",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Ocurrio un error desconocido al obtener el remitente de la base",
                error_details=str(e)
            ) from e
