from typing import List, Dict, Any
from sqlmodel import Session, select, or_, func
from src.db.database import engine
from src.model.entity.ambito import Ambito

class AmbitoRepository:

    @staticmethod
    def add_ambito(ambito: Ambito) -> Ambito:
        with Session(engine) as session:
            session.add(ambito)
            session.commit()
            session.refresh(ambito)
        return ambito


    @staticmethod
    def get_all_ambient() -> List[Ambito]:
        with Session(engine) as session:
            ambitos = session.exec(select(Ambito)).all()
        return ambitos


    @staticmethod
    def update_ambito(ambito: Ambito) -> Ambito:
        with Session(engine) as session:
            session.add(ambito)
            session.commit()
            session.refresh(ambito)
        return ambito


    @staticmethod
    def delete_ambito_by_id(ambito_id: int) -> None:
        with Session(engine) as session:
            ambito = session.get(Ambito, ambito_id)
            if ambito:
                session.delete(ambito)
                session.commit()


    @staticmethod
    def get_ambito_by_id(ambito_id: int) -> Ambito:
        with Session(engine) as session:
            ambito = session.get(Ambito, ambito_id)
        return ambito


    @staticmethod
    def exists(nombre_ambito: str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Ambito).where(Ambito.nombre_ambito == nombre_ambito)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[Ambito]:
        with Session(engine) as session:
            search_filter = or_(
                Ambito.nombre_ambito.contains(search_string)
            )
            ambitos = session.exec(select(Ambito).where(search_filter)).all()
        return ambitos


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
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