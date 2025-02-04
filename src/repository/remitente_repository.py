from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func, or_, Text
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.remitente import Remitente

class RemitenteRepository:

    @staticmethod
    def add_remitentes(remitente: Remitente) -> Remitente:
        with Session(engine) as session:
            try:
                session.add(remitente)
                session.commit()
                session.refresh(remitente)
                return remitente
            except SQLAlchemyError as e:
                raise DatabaseException("Error al registrar el remitente en la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al registrar el remitente en la base") from e


    @staticmethod
    def get_all() -> List[Remitente]:
        with Session(engine) as session:
            try:
                remitentes = session.exec(select(Remitente)).all()
                return list(remitentes)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los remitentes de la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los remitentes de la base") from e


    @staticmethod
    def update_remitente(remitente: Remitente) -> Remitente:
        with Session(engine) as session:
            try:
                session.add(remitente)
                session.commit()
                session.refresh(remitente)
                return remitente
            except SQLAlchemyError as e:
                raise DatabaseException("Error al actualizar el remitente en la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al actualizar el remitente en la base") from e


    @staticmethod
    def delete_by_id(remitente_id: int) -> None:
        with Session(engine) as session:
            try:
                remitente = session.get(Remitente, remitente_id)
                if remitente:
                    session.delete(remitente)
                    session.commit()
            except SQLAlchemyError as e:
                raise DatabaseException("Error al eliminar el remitente de la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al eliminar el remitente de la base") from e


    @staticmethod
    def get_by_id(remitente_id: int) -> Optional[Remitente]:
        with Session(engine) as session:
            try:
                remitente = session.get(Remitente, remitente_id)
                return remitente
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el remitente de la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el remitente de la base") from e


    @staticmethod
    def exists(dni: int) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(select(Remitente).where(Remitente.dni == dni)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del remitente en la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del remitente en la base") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Remitente]:
        with Session(engine) as session:
            try:
                search_filter = or_(
                    Remitente.nombres.contains(search_string),
                    Remitente.apellido_paterno.contains(search_string),
                    func.cast(Remitente.dni, Text).contains(search_string)
                )
                remitentes = session.exec(select(Remitente).where(search_filter)).all()
                return list(remitentes)
            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar los remitentes en la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar los remitentes en la base") from e


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                remitentes = session.exec(
                    select(Remitente)
                    .order_by(Remitente.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()
                total_items = session.exec(select(func.count()).select_from(Remitente)).first()
                total_pages = (total_items + page_size - 1) // page_size

                return {
                    "data": remitentes,
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": total_items,
                        "total_pages": total_pages
                    }
                }
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los remitentes de la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los remitentes de la base") from e


    @staticmethod
    def get_by_dni(dni: int) -> Remitente | None:
        with Session(engine) as session:
            try:
                remitente = session.exec(select(Remitente).where(Remitente.dni == dni)).first()
                return remitente
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el remitente de la base") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el remitente de la base") from e









