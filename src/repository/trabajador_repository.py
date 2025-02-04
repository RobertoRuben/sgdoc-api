from typing import List, Dict, Any, Optional
from sqlmodel import Session, select, func, or_, Text, text, cast
from src.exception import DatabaseException
from sqlalchemy.exc import SQLAlchemyError
from src.db.database import engine
from src.model.entity.trabajador import Trabajador
from src.model.entity.area import Area

class TrabajadorRepository:

    @staticmethod
    def add_trabajador(trabajador: Trabajador) -> Trabajador:
        with Session(engine) as session:
            try:
                session.add(trabajador)
                session.commit()
                session.refresh(trabajador)
                return trabajador
            except SQLAlchemyError as e:
                raise DatabaseException("Error al guardar el trabajador en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def get_trabajadores_with_area_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                result = session.exec(
                    select(Trabajador.id, Trabajador.dni, Trabajador.nombres, Trabajador.apellido_paterno,
                           Trabajador.apellido_materno, Trabajador.genero, Area.nombre_area)
                    .join(Area, Trabajador.area_id == Area.id)
                    .order_by(Trabajador.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()

                trabajadores_data = [dict(row._mapping) for row in result]
                total_items = session.exec(select(func.count()).select_from(Trabajador)).first()
                total_pages = (total_items + page_size - 1) // page_size

                return {
                    "data": trabajadores_data,
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": total_items,
                        "total_pages": total_pages
                    }
                }
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los trabajadores de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def get_all_id_and_name() -> List[Dict[str, Any]]:
        with Session(engine) as session:
            try:
                query = text("""
                    SELECT fn_trabajadores_listar()
                """)
                connection = session.connection()
                result = connection.execute(query).scalar()

                return result if result else []
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los trabajadores de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def update_trabajador(trabajador: Trabajador) -> Trabajador:
        with Session(engine) as session:
            try:
                session.add(trabajador)
                session.commit()
                session.refresh(trabajador)
                return trabajador
            except SQLAlchemyError as e:
                raise DatabaseException("Error al actualizar el trabajador en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def delete_by_id(trabajador_id: int) -> None:
        with Session(engine) as session:
            try:
                trabajador = session.get(Trabajador, trabajador_id)
                if trabajador:
                    session.delete(trabajador)
                    session.commit()
            except SQLAlchemyError as e:
                raise DatabaseException("Error al eliminar el trabajador de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def get_by_id(trabajador_id: int) -> Optional[Trabajador]:
        with Session(engine) as session:
            try:
                trabajador = session.get(Trabajador, trabajador_id)
                return trabajador
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el trabajador de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def exists_trabajador_by_dni(dni: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Trabajador).where(Trabajador.dni == dni)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del trabajador en la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Dict[str, Any]]:
        with Session(engine) as session:
            try:
                search_filter = or_(
                    cast(Trabajador.dni, Text).contains(search_string),
                    Trabajador.nombres.contains(search_string),
                    Trabajador.apellido_paterno.contains(search_string),
                    Trabajador.apellido_materno.contains(search_string)
                )
                result = session.exec(
                    select(Trabajador.id, Trabajador.dni, Trabajador.nombres, Trabajador.apellido_paterno,
                           Trabajador.apellido_materno, Trabajador.genero, Area.nombre_area)
                    .join(Area, Trabajador.area_id == Area.id)
                    .where(search_filter)
                ).all()

                trabajadores_data = [dict(row._mapping) for row in result]

                return trabajadores_data
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los trabajadores de la base de datos") from e
            except Exception as e:
                raise DatabaseException("Error inesperado en la base de datos") from e