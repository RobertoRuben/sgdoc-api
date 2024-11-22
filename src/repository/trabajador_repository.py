from typing import List, Dict, Any, Optional
from sqlmodel import Session, select, func, or_, Text, text, cast
from src.db.database import engine
from src.model.entity.trabajador import Trabajador
from src.model.entity.area import Area

class TrabajadorRepository:

    @staticmethod
    def add_trabajador(trabajador: Trabajador) -> Trabajador:
        with Session(engine) as session:
            session.add(trabajador)
            session.commit()
            session.refresh(trabajador)
        return trabajador

    @staticmethod
    def get_trabajadores_with_area_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
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


    @staticmethod
    def get_all_id_and_name() -> List[Dict[str, Any]]:
        with Session(engine) as session:
            query = text("""
                SELECT fn_listar_trabajadores()
            """)
            connection = session.connection()
            result = connection.execute(query).scalar()

            return result if result else []


    @staticmethod
    def update_trabajador(trabajador: Trabajador) -> Trabajador:
        with Session(engine) as session:
            session.add(trabajador)
            session.commit()
            session.refresh(trabajador)
        return trabajador


    @staticmethod
    def delete_by_id(trabajador_id: int) -> None:
        with Session(engine) as session:
            trabajador = session.get(Trabajador, trabajador_id)
            if trabajador:
                session.delete(trabajador)
                session.commit()


    @staticmethod
    def get_by_id(trabajador_id: int) -> Optional[Trabajador]:
        with Session(engine) as session:
            trabajador = session.get(Trabajador, trabajador_id)
        return trabajador


    @staticmethod
    def exists_trabajador_by_dni(dni: int) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Trabajador).where(Trabajador.dni == dni)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[Dict[str, Any]]:
        with Session(engine) as session:
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