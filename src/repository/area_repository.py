from typing import List, Dict, Any
from sqlmodel import Session, select, or_, func
from sqlalchemy.exc import SQLAlchemyError
from src.exception import DatabaseException
from src.db.database import engine
from src.model.entity.area import Area

class AreaRepository:

    @staticmethod
    def add_area(area: Area) -> Area:
        try:
            with Session(engine) as session:
                session.add(area)
                session.commit()
                session.refresh(area)
            return area
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Error al agregar el área") from e
        except Exception as e:
            session.rollback()
            raise DatabaseException("Error desconocido al agregar el área") from e


    @staticmethod
    def get_all_areas() -> List[Area]:
        try:
            with Session(engine) as session:
                areas = session.exec(select(Area)).all()
            return areas
        except SQLAlchemyError as e:
            raise DatabaseException("Error al obtener las áreas") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al obtener las áreas") from e


    @staticmethod
    def update_area(area: Area) -> Area:
        try:
            with Session(engine) as session:
                session.add(area)
                session.commit()
                session.refresh(area)
            return area
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Error al actualizar el área") from e
        except Exception as e:
            session.rollback()
            raise DatabaseException("Error desconocido al actualizar el área") from e


    @staticmethod
    def delete_area_by_id(area_id: int) -> None:
        try:
            with Session(engine) as session:
                area = session.get(Area, area_id)
                if area:
                    session.delete(area)
                    session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Error al eliminar el área") from e
        except Exception as e:
            session.rollback()
            raise DatabaseException("Error desconocido al eliminar el área") from e


    @staticmethod
    def get_area_by_id(area_id: int) -> Area:
        try:
            with Session(engine) as session:
                area = session.get(Area, area_id)
            return area
        except SQLAlchemyError as e:
            raise DatabaseException("Error al obtener el área por ID") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al obtener el área por ID") from e


    @staticmethod
    def exists(nombre_area: str) -> bool:
        try:
            with Session(engine) as session:
                exists = session.exec(
                    select(Area).where(Area.nombre_area == nombre_area)
                ).first() is not None
            return exists
        except SQLAlchemyError as e:
            raise DatabaseException("Error al verificar la existencia del área") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al verificar la existencia del área") from e


    @staticmethod
    def exists_by_id(area_id: int) -> bool:
        try:
            with Session(engine) as session:
                exists = session.get(Area, area_id) is not None
            return exists
        except SQLAlchemyError as e:
            raise DatabaseException("Error al verificar la existencia del área por ID") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al verificar la existencia del área por ID") from e


    @staticmethod
    def find_by_string(search_string: str) -> List[Area]:
        try:
            with Session(engine) as session:
                search_filter = or_(Area.nombre_area.contains(search_string))
                areas = session.exec(select(Area).where(search_filter)).all()
            return areas
        except SQLAlchemyError as e:
            raise DatabaseException("Error al buscar áreas por cadena") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al buscar áreas por cadena") from e


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        try:
            with Session(engine) as session:
                areas = session.exec(
                    select(Area)
                    .order_by(Area.id)
                    .offset(offset)
                    .limit(page_size)
                ).all()
                total_items = session.exec(select(func.count()).select_from(Area)).first()
                total_pages = (total_items + page_size - 1) // page_size
            return {
                "data": areas,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages
                }
            }
        except SQLAlchemyError as e:
            raise DatabaseException("Error al obtener las áreas paginadas") from e
        except Exception as e:
            raise DatabaseException("Error desconocido al obtener las áreas paginadas") from e
