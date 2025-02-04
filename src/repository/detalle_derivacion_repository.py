from typing import List, Tuple, Optional
from sqlmodel import  Session, select, func, or_
from sqlalchemy.exc import SQLAlchemyError
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.detalle_derivacion import DetalleDerivacion
from src.model.entity.usuario import Usuario

class DetalleDerivacionRepository:

    @staticmethod
    def add_detalle_derivacion(detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        with Session(engine) as session:
            try:
                session.add(detalle_derivacion)
                session.commit()
                session.refresh(detalle_derivacion)
                return detalle_derivacion
            except SQLAlchemyError as e:
                raise DatabaseException("Error al guardar el detalle de derivación en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al guardar el detalle de derivación en la base de datos") from e


    @staticmethod
    def get_all_by_derivacion_id(derivacion_id: int) -> List[Tuple[DetalleDerivacion, str]]:
        with Session(engine) as session:
            try:
                query = (
                    select(DetalleDerivacion, Usuario.nombre_usuario)
                    .join(Usuario, DetalleDerivacion.usuario_id == Usuario.id, isouter=True)
                    .where(DetalleDerivacion.derivacion_id == derivacion_id)
                    .order_by(DetalleDerivacion.id.desc())
                )
                resultados = session.exec(query).all()
                return list(resultados)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los detalles de derivación de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los detalles de derivación de la base de datos") from e


    @staticmethod
    def update_detalle_derivacion(detalle_derivacion: DetalleDerivacion) -> DetalleDerivacion:
        with Session(engine) as session:
            try:
                session.add(detalle_derivacion)
                session.commit()
                session.refresh(detalle_derivacion)
                return detalle_derivacion
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar el detalle de derivación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar el detalle de derivación en la base de datos") from e


    @staticmethod
    def delete_by_id(detalle_derivacion_id: int) -> None:
        with Session(engine) as session:
            try:
                detalle_derivacion = session.get(DetalleDerivacion, detalle_derivacion_id)
                if detalle_derivacion:
                    session.delete(detalle_derivacion)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al eliminar el detalle de derivación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al eliminar el detalle de derivación en la base de datos") from e


    @staticmethod
    def exists_detalle_derivacion_by_id(detalle_derivacion_id: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.get(DetalleDerivacion, detalle_derivacion_id) is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del detalle de derivación en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del detalle de derivación en la base de datos") from e


    @staticmethod
    def get_by_id(detalle_derivacion_id: int) -> Optional[DetalleDerivacion]:
        with Session(engine) as session:
            try:
                detalle_derivacion = session.get(DetalleDerivacion, detalle_derivacion_id)
                return detalle_derivacion
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el detalle de derivación de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el detalle de derivación de la base de datos") from e
