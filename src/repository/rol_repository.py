from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func, or_, Text
from src.model.entity.rol import Rol
from src.db.database import engine

class RolRepository:

    @staticmethod
    def add_rol(rol: Rol) -> Rol:
        with Session(engine) as session:
            session.add(rol)
            session.commit()
            session.refresh(rol)
        return rol


    @staticmethod
    def get_all() -> List[Rol]:
        with Session(engine) as session:
            roles = session.exec(select(Rol)).all()
        return roles


    @staticmethod
    def update_rol(rol: Rol) -> Rol:
        with Session(engine) as session:
            session.add(rol)
            session.commit()
            session.refresh(rol)
        return rol


    @staticmethod
    def delete_by_id(rol_id: int) -> None:
        with Session(engine) as session:
            rol = session.get(Rol, rol_id)
            if rol:
                session.delete(rol)
                session.commit()


    @staticmethod
    def get_by_id(rol_id: int) -> Optional[Rol]:
        with Session(engine) as session:
            rol = session.get(Rol, rol_id)
        return rol


    @staticmethod
    def exists(nombre_rol: str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Rol).where(Rol.nombre_rol == nombre_rol)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[Rol]:
        with Session(engine) as session:
            search_filter = or_(
                Rol.nombre_rol.contains(search_string),
                func.cast(Rol.id, Text).contains(search_string)
            )
            roles = session.exec(select(Rol).where(search_filter)).all()
        return roles


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            roles = session.exec(
                select(Rol)
                .order_by(Rol.id)
                .offset(offset)
                .limit(page_size)
            ).all()
            total_items = session.exec(select(func.count()).select_from(Rol)).first()
            total_pages = (total_items + page_size - 1) // page_size

        return {
            "data": roles,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }

