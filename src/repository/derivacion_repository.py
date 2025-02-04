from typing import Dict, Any, Optional
from sqlmodel import Session, text
from sqlalchemy.exc import SQLAlchemyError
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.derivacion import Derivacion

class DerivacionRepository:

    @staticmethod
    def add(derivacion: Derivacion) -> Derivacion:
        with Session(engine) as session:
            try:
                session.add(derivacion)
                session.commit()
                session.refresh(derivacion)
                return derivacion
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al guardar la derivación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al guardar la derivación en la base de datos") from e


    @staticmethod
    def get_all(
        page: int = 1,
        page_size: int = 10,
        fecha_filtro: str = None,
        estado_filtro: str = None,
        documento_id_filtro: int = None
    ) -> Dict[str, Any]:
        with Session(engine) as session:
            try:
                query = text("""
                    SELECT fn_derivaciones_filtrar_paginated(:page, :page_size, :fecha_filtro, :estado_filtro, :documento_id_filtro)
                """)
                connection = session.connection()
                result = connection.execute(query, {
                    "page": page,
                    "page_size": page_size,
                    "fecha_filtro": fecha_filtro,
                    "estado_filtro": estado_filtro,
                    "documento_id_filtro": documento_id_filtro
                }).scalar()

                return result if result else {
                    "data": [],
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener las derivaciones de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener las derivaciones de la base de datos") from e


    @staticmethod
    def update(derivacion: Derivacion) -> Derivacion:
        with Session(engine) as session:
            try:
                session.add(derivacion)
                session.commit()
                session.refresh(derivacion)
                return derivacion
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar la derivación en la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar la derivación en la base de datos") from e


    @staticmethod
    def delete_by_id(derivacion_id: int) -> None:
        with Session(engine) as session:
            try:
                derivacion = session.get(Derivacion, derivacion_id)
                if derivacion:
                    session.delete(derivacion)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al eliminar la derivación de la base de datos") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al eliminar la derivación de la base de datos") from e


    @staticmethod
    def get_by_id(derivacion_id: int) -> Optional[Derivacion]:
        with Session(engine) as session:
            try:
                derivacion = session.get(Derivacion, derivacion_id)
                return derivacion
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener la derivación de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener la derivación de la base de datos") from e


    @staticmethod
    def exists_by_id(derivacion_id: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.get(Derivacion, derivacion_id) is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia de la derivación en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia de la derivación en la base de datos") from e
