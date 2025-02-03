from typing import List, Dict, Any, Optional
from sqlmodel import Session, select, or_, func
from sqlalchemy.exc import SQLAlchemyError
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.ambito import Ambito

class AmbitoRepository:

    @staticmethod
    def add_ambito(ambito: Ambito) -> Ambito:
        with Session(engine) as session:
            try:
                session.add(ambito)
                session.commit()
                session.refresh(ambito)
                return ambito
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al agregar el ambito") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al agregar el ambito") from e


    @staticmethod
    def get_all_ambient() -> List[Ambito]:
        with Session(engine) as session:
            try:
                ambitos = session.exec(select(Ambito)).all()
                return ambitos
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los ambitos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los ambitos") from e


    @staticmethod
    def update_ambito(ambito: Ambito) -> Ambito:
        with Session(engine) as session:
            try:
                session.add(ambito)
                session.commit()
                session.refresh(ambito)
                return ambito
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar el ambito") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar el ambito") from e


    @staticmethod
    def delete_ambito_by_id(ambito_id: int) -> None:
        with Session(engine) as session:
            try:
                ambito = session.get(Ambito, ambito_id)
                if ambito:
                    session.delete(ambito)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al eliminar el ambito") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al eliminar el ambito") from e


    @staticmethod
    def get_ambito_by_id(ambito_id: int) -> Optional[Ambito]:
        with Session(engine) as session:
            try:
                ambito = session.get(Ambito, ambito_id)
                return ambito
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el ambito por ID") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el ambito por ID") from e


    @staticmethod
    def exists(nombre_ambito: str) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(
                    select(Ambito).where(Ambito.nombre_ambito == nombre_ambito)
                ).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del ambito") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del ambito") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Ambito]:
        with Session(engine) as session:
            try:
                search_filter = or_(Ambito.nombre_ambito.contains(search_string))
                ambitos = session.exec(select(Ambito).where(search_filter)).all()
                return ambitos
            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar ambitos por cadena") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar ambitos por cadena") from e


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                ambitos = session.exec(
                    select(Ambito)
                    .order_by(Ambito.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()
                total_items = session.exec(select(func.count()).select_from(Ambito)).first()
                total_pages = (total_items + page_size - 1) // page_size

                return {
                    "data": ambitos,
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": total_items,
                        "total_pages": total_pages
                    }
                }
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los ambitos paginados") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los ambitos paginados") from e
