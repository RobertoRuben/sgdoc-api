from typing import Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Derivacion

class DerivacionRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add(self, derivacion: Derivacion) -> Derivacion:
        try:
            self.session.add(derivacion)
            await self.session.commit()
            await self.session.refresh(derivacion)
            return derivacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al guardar la derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al guardar la derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def get_paginated(
            self,
            page: int = 1,
            page_size: int = 10,
            fecha_filtro: Optional[str] = None,
            estado_filtro: Optional[str] = None,
            documento_id_filtro: Optional[int] = None
    ) -> Dict[str, Any]:
        try:
            query = text("""
                SELECT fn_derivaciones_filtrar_paginated(
                    :page, 
                    :page_size, 
                    :fecha_filtro, 
                    :estado_filtro, 
                    :documento_id_filtro
                )
            """)
            async with self.session.connection() as connection:
                result = await connection.execute(query, {
                    "page": page,
                    "page_size": page_size,
                    "fecha_filtro": fecha_filtro,
                    "estado_filtro": estado_filtro,
                    "documento_id_filtro": documento_id_filtro
                })
                derivaciones = result.scalar()

            return derivaciones if derivaciones else {
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
                "Error al obtener las derivaciones de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener las derivaciones de la base de datos",
                error_details=str(e)
            ) from e


    async def update(self, derivacion: Derivacion) -> Derivacion:
        try:
            self.session.add(derivacion)
            await self.session.commit()
            await self.session.refresh(derivacion)
            return derivacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al actualizar la derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al actualizar la derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, derivacion_id: int) -> None:
        try:
            derivacion = await self.session.get(Derivacion, derivacion_id)
            if derivacion:
                await self.session.delete(derivacion)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al eliminar la derivación de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al eliminar la derivación de la base de datos",
                error_details=str(e)
            ) from e


    async def get_by_id(self, derivacion_id: int) -> Optional[Derivacion]:
        try:
            derivacion = await self.session.get(Derivacion, derivacion_id)
            return derivacion
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al obtener la derivación de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al obtener la derivación de la base de datos",
                error_details=str(e)
            ) from e


    async def exists_by_id(self, derivacion_id: int) -> bool:
        try:
            derivacion = await self.session.get(Derivacion, derivacion_id)
            return derivacion is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Error al verificar la existencia de la derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Error desconocido al verificar la existencia de la derivación en la base de datos",
                error_details=str(e)
            ) from e
