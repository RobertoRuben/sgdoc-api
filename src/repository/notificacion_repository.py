from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.exception import DatabaseException
from src.db.database import get_async_session
from src.model.entity import Notificacion

class NotificacionRepository:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_notificacion(self, notificacion: Notificacion) -> Notificacion:
        try:
            self.session.add(notificacion)
            await self.session.commit()
            await self.session.refresh(notificacion)
            return notificacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al crear la notificación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al crear la notificación en la base de datos",
                error_details=str(e)
            ) from e


    async def get_notificaciones_by_area_destino_id(self, area_destino_id: int) -> List[Notificacion]:
        try:
            statement = select(Notificacion).where(Notificacion.area_destino_id == area_destino_id)
            result = await self.session.exec(statement)
            notificaciones = result.all()
            return notificaciones
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener las notificaciones de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener las notificaciones de la base de datos",
                error_details=str(e)
            ) from e


    async def get_notificacion_by_id(self, notificacion_id: int) -> Optional[Notificacion]:
        try:
            notificacion = await self.session.get(Notificacion, notificacion_id)
            return notificacion
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al obtener la notificación de la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al obtener la notificación de la base de datos",
                error_details=str(e)
            ) from e


    async def mark_notification_as_read(self, notificacion_id: int) -> Notificacion:
        try:
            notificacion = await self.session.get(Notificacion, notificacion_id)
            if notificacion:
                notificacion.leido = True
                self.session.add(notificacion)
                await self.session.commit()
                await self.session.refresh(notificacion)
            return notificacion
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error al actualizar la notificación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(
                "Error desconocido al actualizar la notificación en la base de datos",
                error_details=str(e)
            ) from e


    async def exists_by_id(self, notificacion_id: int) -> bool:
        try:
            notificacion = await self.session.get(Notificacion, notificacion_id)
            return notificacion is not None
        except SQLAlchemyError as e:
            raise DatabaseException(
                "Error al verificar la existencia de la notificación en la base de datos",
                error_details=str(e)
            ) from e
        except Exception as e:
            raise DatabaseException(
                "Error desconocido al verificar la existencia de la notificación en la base de datos",
                error_details=str(e)
            ) from e
