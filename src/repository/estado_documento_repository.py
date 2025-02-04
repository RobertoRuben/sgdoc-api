from typing import Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.estado_documento import EstadoDocumento

class EstadoDocumentoRepository:

    @staticmethod
    def add_estado_documento(estado_documento: EstadoDocumento) -> EstadoDocumento:
        with Session(engine) as session:
            try:
                session.add(estado_documento)
                session.commit()
                session.refresh(estado_documento)
                return estado_documento
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al guardar el estado del documento en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido en la base de datos") from e


    @staticmethod
    def get_all_estado_documento(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                documentos = session.exec(
                    select(EstadoDocumento)
                    .order_by(EstadoDocumento.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()
                total_items = session.exec(select(func.count()).select_from(EstadoDocumento)).first()
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
                raise DatabaseException("Error al obtener los estados de los documentos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido en la base de datos") from e


    @staticmethod
    def update_estado_documento(estado_documento: EstadoDocumento) -> EstadoDocumento:
        with Session(engine) as session:
            try:
                session.add(estado_documento)
                session.commit()
                session.refresh(estado_documento)
                return estado_documento
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar el estado del documento en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido en la base de datos") from e


    @staticmethod
    def delete_by_id(estado_documento_id: int):
        with Session(engine) as session:
            try:
                estado_documento = session.get(EstadoDocumento, estado_documento_id)
                if estado_documento:
                    session.delete(estado_documento)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al eliminar el estado del documento en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido en la base de datos") from e


    @staticmethod
    def get_estado_documento_by_id(estado_documento_id: int) -> EstadoDocumento:
        with Session(engine) as session:
            try:
                estado_documento = session.exec(select(EstadoDocumento).where(EstadoDocumento.id == estado_documento_id)).first()
                return estado_documento
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el estado del documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido en la base de datos") from e


    def get_all_estados_by_id(self, documento_id: int) -> List[EstadoDocumento]:
        with Session(engine) as session:
            try:
                estado_documento = session.exec(
                    select(EstadoDocumento).where(EstadoDocumento.documento_id == documento_id)).all()
                return estado_documento
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los estados del documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido en la base de datos") from e


    @staticmethod
    def exits_estado_documento_by_id(estado_documento_id: int) -> bool:
        with Session(engine) as session:
            try:
                estado_documento = session.exec(
                    select(EstadoDocumento).where(EstadoDocumento.id == estado_documento_id)).first()
                return estado_documento is not None
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar si existe el estado del documento") from e
            except Exception as e:
                raise DatabaseException("Error desconocido en la base de datos") from e
