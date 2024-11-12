from typing import List, Optional, Dict, Any
from src.db.database import engine
from sqlmodel import Session, select, func, or_
from src.model.entity.centro_poblado import CentroPoblado

class CentroPobladoRepository:

    @staticmethod
    def add_centro_poblado(centro_poblado: CentroPoblado) -> CentroPoblado:
        with Session(engine) as session:
            session.add(centro_poblado)
            session.commit()
            session.refresh(centro_poblado)
        return centro_poblado


    @staticmethod
    def get_all() -> List[CentroPoblado]:
        with Session(engine) as session:
            centro_poblados = session.exec(select(CentroPoblado)).all()
        return centro_poblados


    @staticmethod
    def update_centro_poblado(centro_poblado: CentroPoblado) -> CentroPoblado:
        with Session(engine) as session:
            session.add(centro_poblado)
            session.commit()
            session.refresh(centro_poblado)
        return centro_poblado


    @staticmethod
    def delete_by_id(centro_poblado_id: int) -> None:
        with Session(engine) as session:
            centro_poblado = session.get(CentroPoblado, centro_poblado_id)
            if centro_poblado:
                session.delete(centro_poblado)
                session.commit()


    @staticmethod
    def get_by_id(centro_poblado_id: int) -> Optional[CentroPoblado]:
        with Session(engine) as session:
            centro_poblado = session.get(CentroPoblado, centro_poblado_id)
        return centro_poblado


    @staticmethod
    def exist(nombre_centro_poblado: str) -> bool:
        with Session(engine) as session:
            exists = session.exec(select(CentroPoblado).where(CentroPoblado.nombre_centro_poblado == nombre_centro_poblado)).first() is not None
        return exists


    @staticmethod
    def find_by_string(search_string: str) -> List[CentroPoblado]:
        with Session(engine) as session:
            search_filter = or_(
                CentroPoblado.nombre_centro_poblado.contains(search_string)
            )
            centro_poblados = session.exec(select(CentroPoblado).where(search_filter)).all()
        return centro_poblados


    @staticmethod
    def get_all_pagination(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        with Session(engine) as session:
            centro_poblados = session.exec(
                select(CentroPoblado)
                .order_by(CentroPoblado.id)
                .offset(offset)
                .limit(page_size)
            ).all()

            total_items = session.exec(select(func.count()).select_from(CentroPoblado)).first()
            total_pages = (total_items + page_size - 1) // page_size

        return {
            "data": centro_poblados,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }