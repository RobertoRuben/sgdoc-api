from typing import Dict, Any, List
from sqlmodel import Session, select, text, func
from src.db.database import engine
from src.model.entity.comunicacion_area import ComunicacionArea

class ComunicacionAreaRepository:

    @staticmethod
    def get_all_paginated(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        with Session(engine) as session:
            query = text("""
                SELECT fn_comunicacion_areas_get_paginated_data(:page, :page_size)
            """)
            connection = session.connection()
            result = connection.execute(query, {"page": page, "page_size": page_size}).scalar()

            if result:
                return result
            else:
                return {
                    "data": [],
                    "pagination": {
                        "current_page": page,
                        "page_size": page_size,
                        "total_items": 0,
                        "total_pages": 0
                    }
                }

    @staticmethod
    def get_areas_destino_by_area_origen_id(area_origen_id: int) -> List[Dict[str, Any]]:
        with Session(engine) as session:
            query = text("""
                SELECT fn_obtener_areas_destino_por_area_origen_id(:area_origen_id)
            """)
            connection = session.connection()
            result = connection.execute(query, {"area_origen_id": area_origen_id}).scalar()

            return result if result else []


