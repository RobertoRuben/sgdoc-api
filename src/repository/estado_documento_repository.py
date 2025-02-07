from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import EstadoDocumento

class EstadoDocumentoRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session


    async def add_estado_documento(self, estado_documento: EstadoDocumento) -> EstadoDocumento:
        try:
            self.session.add(estado_documento)
            await self.session.commit()
            await self.session.refresh(estado_documento)
            return estado_documento
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al guardar el estado del documento en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def get_all_estado_documento(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            result = await self.session.exec(
                select(EstadoDocumento)
                .order_by(EstadoDocumento.id)
                .offset(offset)
                .limit(page_size)
            )
            documentos = result.all()
            total_result = await self.session.exec(
                select(func.count()).select_from(EstadoDocumento)
            )
            total_items = total_result.first() or 0
            total_pages = (total_items + page_size - 1) // page_size

            return {
                "data": documentos,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener los estados de los documentos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def update_estado_documento(self, estado_documento: EstadoDocumento) -> EstadoDocumento:
        try:
            self.session.add(estado_documento)
            await self.session.commit()
            await self.session.refresh(estado_documento)
            return estado_documento
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar el estado del documento en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, estado_documento_id: int) -> None:
        try:
            estado_documento = await self.session.get(EstadoDocumento, estado_documento_id)
            if estado_documento:
                await self.session.delete(estado_documento)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al eliminar el estado del documento en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def get_estado_documento_by_id(self, estado_documento_id: int) -> Optional[EstadoDocumento]:
        try:
            result = await self.session.exec(
                select(EstadoDocumento).where(EstadoDocumento.id == estado_documento_id)
            )
            estado_documento = result.first()
            return estado_documento
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener el estado del documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def get_all_estados_by_id(self, documento_id: int) -> List[EstadoDocumento]:
        try:
            result = await self.session.exec(
                select(EstadoDocumento).where(EstadoDocumento.documento_id == documento_id)
            )
            estado_documentos = result.all()
            return estado_documentos
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener los estados del documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e


    async def exists_estado_documento_by_id(self, estado_documento_id: int) -> bool:
        try:
            result = await self.session.exec(
                select(EstadoDocumento).where(EstadoDocumento.id == estado_documento_id)
            )
            estado_documento = result.first()
            return estado_documento is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar si existe el estado del documento",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido en la base de datos",
                error_details=str(e)
            ) from e
