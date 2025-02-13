from typing import List, Tuple, Optional
from sqlmodel import select, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import DetalleDerivacion, Usuario

class DetalleDerivacionRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_detalle_derivacion(self, detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        try:
            self.session.add(detalle_derivacion)
            await self.session.commit()
            await self.session.refresh(detalle_derivacion)
            return detalle_derivacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al guardar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al guardar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def get_all_by_derivacion_id(self, derivacion_id: int) -> List[Tuple[DetalleDerivacion, str]]:
        try:
            query = (
                select(DetalleDerivacion, Usuario.nombre_usuario)
                .join(Usuario, DetalleDerivacion.usuario_id == Usuario.id, isouter=True)
                .where(DetalleDerivacion.derivacion_id == derivacion_id)
                .order_by(DetalleDerivacion.id.desc())
            )
            result = await self.session.exec(query)
            resultados = result.all()
            return list(resultados)
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener los detalles de derivación de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener los detalles de derivación de la base de datos",
                error_details=str(e)
            ) from e


    async def update_detalle_derivacion(self, detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        try:
            self.session.add(detalle_derivacion)
            await self.session.commit()
            await self.session.refresh(detalle_derivacion)
            return detalle_derivacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error al actualizar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Error desconocido al actualizar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, detalle_derivacion_id: int) -> None:
        try:
            detalle_derivacion = await self.session.get(DetalleDerivacion, detalle_derivacion_id)
            if detalle_derivacion:
                await self.session.delete(detalle_derivacion)
                await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error al eliminar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                detail="Ocurrio un error desconocido al eliminar el detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def exists_detalle_derivacion_by_id(self, detalle_derivacion_id: int) -> bool:
        try:
            detalle = await self.session.get(DetalleDerivacion, detalle_derivacion_id)
            return detalle is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al verificar la existencia del detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al verificar la existencia del detalle de derivación en la base de datos",
                error_details=str(e)
            ) from e


    async def get_by_id(self, detalle_derivacion_id: int) -> Optional[DetalleDerivacion]:
        try:
            detalle_derivacion = await self.session.get(DetalleDerivacion, detalle_derivacion_id)
            return detalle_derivacion
        except SQLAlchemyError as e:
            raise DatabaseException(
                detail="Ocurrio un error al obtener el detalle de derivación de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                detail="Ocurrio un error desconocido al obtener el detalle de derivación de la base de datos",
                error_details=str(e)
            ) from e
