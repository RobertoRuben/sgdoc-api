from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, func, or_
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.caserio import Caserio
from src.model.entity.centro_poblado import CentroPoblado

class CaserioRepository:

    @staticmethod
    def add_caserio(caserio: Caserio) -> Caserio:
        with Session(engine) as session:
            try:
                session.add(caserio)
                session.commit()
                session.refresh(caserio)
                return caserio
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al agregar el caserío") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al agregar el caserío") from e


    @staticmethod
    def get_caserios_names() -> List[Caserio]:
        with Session(engine) as session:
            try:
                caserios = session.exec(
                    select(Caserio.id, Caserio.nombre_caserio)
                    .where(Caserio.centro_poblado_id == None)
                ).all()
                return caserios
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los caseríos") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los caseríos") from e


    @staticmethod
    def update_caserio(caserio: Caserio) -> Caserio:
        with Session(engine) as session:
            try:
                session.add(caserio)
                session.commit()
                session.refresh(caserio)
                return caserio
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al actualizar el caserío") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al actualizar el caserío") from e


    @staticmethod
    def delete_caserio_by_id(caserio_id: int) -> None:
        with Session(engine) as session:
            try:
                caserio = session.get(Caserio, caserio_id)
                if caserio:
                    session.delete(caserio)
                    session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseException("Error al eliminar el caserío") from e
            except Exception as e:
                session.rollback()
                raise DatabaseException("Error desconocido al eliminar el caserío") from e


    @staticmethod
    def get_caserio_by_id(caserio_id: int) -> Optional[Caserio]:
        with Session(engine) as session:
            try:
                caserio = session.get(Caserio, caserio_id)
                return caserio
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener el caserío") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener el caserío") from e


    @staticmethod
    def exists(nombre_caserio: str) -> bool:
        with Session(engine) as session:
            try:
                exists = session.exec(
                    select(Caserio).where(Caserio.nombre_caserio == nombre_caserio)).first() is not None
                return exists
            except SQLAlchemyError as e:
                raise DatabaseException("Error al verificar la existencia del caserío") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al verificar la existencia del caserío") from e


    @staticmethod
    def get_all_caserios_by_centro_poblado_id(centro_poblado_id: int | None) -> List[Caserio]:
        with Session(engine) as session:
            try:
                if centro_poblado_id is not None:
                    caserios = session.exec(select(Caserio).where(Caserio.centro_poblado_id == centro_poblado_id)).all()
                else:
                    caserios = session.exec(select(Caserio)).all()
                return caserios
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los caseríos por ID de centro poblado") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los caseríos por ID de centro poblado") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Dict[str, Any]]:
        with Session(engine) as session:
            try:
                search_filter = or_(Caserio.nombre_caserio.contains(search_string))
                result = session.exec(
                    select(Caserio.id, Caserio.nombre_caserio, CentroPoblado.nombre_centro_poblado)
                    .join(CentroPoblado, Caserio.centro_poblado_id == CentroPoblado.id, isouter=True)
                    .where(search_filter)
                ).all()
                caserios_data = [dict(row._mapping) for row in result]
                return caserios_data

            except SQLAlchemyError as e:
                raise DatabaseException("Error al buscar los caseríos por nombre") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al buscar los caseríos por nombre") from e


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            try:
                result = session.exec(
                    select(Caserio.id, Caserio.nombre_caserio, CentroPoblado.nombre_centro_poblado)
                    .join(CentroPoblado, Caserio.centro_poblado_id == CentroPoblado.id, isouter=True)
                    .order_by(Caserio.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()

                caserios_data = [dict(row._mapping) for row in result]

                total_items = session.exec(select(func.count()).select_from(Caserio)).first()
                total_pages = (total_items + page_size - 1) // page_size

                return {
                    "data": caserios_data,
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": total_items,
                        "total_pages": total_pages
                    }
                }
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener los caseríos con paginación") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener los caseríos con paginación") from e

