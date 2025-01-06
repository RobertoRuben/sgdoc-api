from typing import Dict, Any, Optional
from sqlmodel import Session, text
from src.db.database import engine
from src.model.entity.derivacion import Derivacion

class DerivacionRepository:

    @staticmethod
    def add(derivacion: Derivacion) -> Derivacion:
        with Session(engine) as session:
            session.add(derivacion)
            session.commit()
            session.refresh(derivacion)
            return derivacion


    @staticmethod
    def get_all_paginated(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""
                SELECT fn_derivaciones_get_paginated_data(:page, :page_size)
            """)
            connection = session.connection()
            result = connection.execute(query, {"page": page, "page_size": page_size}).scalar()

            return result if result else {
                "data": [],
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_items": 0,
                    "total_pages": 0
                }
            }


    @staticmethod
    def update(derivacion: Derivacion) -> Derivacion:
        with Session(engine) as session:
            session.add(derivacion)
            session.commit()
            session.refresh(derivacion)
            return derivacion


    @staticmethod
    def delete_by_id(derivacion_id: int) -> None:
        with Session(engine) as session:
            derivacion = session.get(Derivacion, derivacion_id)
            if derivacion:
                session.delete(derivacion)
                session.commit()


    @staticmethod
    def get_by_id(derivacion_id: int) -> Optional[Derivacion]:
        with Session(engine) as session:
            derivacion = session.get(Derivacion, derivacion_id)
        return derivacion


