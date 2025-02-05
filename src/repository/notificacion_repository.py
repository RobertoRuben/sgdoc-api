from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import engine
from src.model.entity.notifcacion import Notificacion
from src.exception import DatabaseException

class NotificacionRepository:

    @staticmethod
    def add_notificacion(notificacion: Notificacion) -> Notificacion:
        with Session(engine) as session:
            try:
                session.add(notificacion)
                session.commit()
                session.refresh(notificacion)
                return notificacion
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al crear la notificación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al crear la notificación en la base de datos") from e


    @staticmethod
    def get_notificaciones_by_area_destino_id(area_destino_id: int) -> List[Notificacion]:
        with Session(engine) as session:
            try:
                statement = select(Notificacion).where(Notificacion.area_destino_id == area_destino_id)
                notificaciones = session.exec(statement).all()
                return notificaciones
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener las notificaciones de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener las notificaciones de la base de datos") from e


    @staticmethod
    def get_notificacion_by_id(notificacion_id: int) -> Optional[Notificacion]:
        with Session(engine) as session:
            try:
                return session.get(Notificacion, notificacion_id)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener la notificación de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener la notificación de la base de datos") from e


    @staticmethod
    def mark_notification_as_read(notificacion_id: int) -> Notificacion:
        with Session(engine) as session:
            try:
                notificacion = session.get(Notificacion, notificacion_id)
                if notificacion:
                    notificacion.leido = True
                    session.add(notificacion)
                    session.commit()
                    session.refresh(notificacion)
                return notificacion
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar la notificación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar la notificación en la base de datos") from e


    @staticmethod
    def exists_by_id(notificacion_id: int) -> bool:
        with Session(engine) as session:
            try:
                notificacion = session.get(Notificacion, notificacion_id)
                return notificacion
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia de la notificación en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia de la notificación en la base de datos") from e
