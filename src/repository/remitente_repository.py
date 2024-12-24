from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, func, or_, Text
from src.db.database import engine
from src.model.entity.remitente import Remitente

class RemitenteRepository:

    @staticmethod
    def add_remitentes(remitente: Remitente) -> Remitente:
        with Session(engine) as session:
            session.add(remitente)
            session.commit()
            session.refresh(remitente)
        return remitente

    @staticmethod
    def get_all() -> List[Remitente]:
        with Session(engine) as session:
            remitentes = session.exec(select(Remitente)).all()
        return remitentes

    @staticmethod
    def update_remitente(remitente: Remitente) -> Remitente:
        with Session(engine) as session:
            session.add(remitente)
            session.commit()
            session.refresh(remitente)
        return remitente


    @staticmethod
    def delete_by_id(remitente_id: int) -> None:
        with Session(engine) as session:
            remitente = session.get(Remitente, remitente_id)
            if remitente:
                session.delete(remitente)
                session.commit()


    @staticmethod
    def get_by_id(remitente_id: int) -> Optional[Remitente]:
        with Session(engine) as session:
            remitente = session.get(Remitente, remitente_id)
        return remitente


    @staticmethod
    def exists(dni: int) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(Remitente).where(Remitente.dni == dni)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[Remitente]:
        with Session(engine) as session:
            search_filter = or_(
                Remitente.nombres.contains(search_string),
                Remitente.apellido_paterno.contains(search_string),
                func.cast(Remitente.dni, Text).contains(search_string)
            )
            remitentes = session.exec(select(Remitente).where(search_filter)).all()
        return remitentes


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
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

    def get_by_dni(self, dni: int) -> Remitente | None:
        with Session(engine) as session:
            return session.exec(select(Remitente).where(Remitente.dni == dni)).first()









