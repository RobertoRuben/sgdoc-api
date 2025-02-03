from typing import Dict, Any, List
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, text
from src.exception import DatabaseException
from src.db.database import engine

class ComunicacionAreaRepository:

    @staticmethod
    def get_all_paginated(page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        with Session(engine) as session:
            try:
                query = text("""
                    SELECT fn_comunicacion_areas_listar_paginado(:page, :page_size)
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
            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener la lista comunicaciones entre areas") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener la lista comunicaciones entre areas") from e


    @staticmethod
    def get_areas_destino_by_area_origen_id(area_origen_id: int) -> List[Dict[str, Any]]:
        with Session(engine) as session:
            try:
                query = text("""
                    SELECT fn_comunicaciones_areas_obtener_area_destino_por_area_origen_id(:area_origen_id)
                """)
                connection = session.connection()
                result = connection.execute(query, {"area_origen_id": area_origen_id}).scalar()

                return result if result else []

            except SQLAlchemyError as e:
                raise DatabaseException("Error al obtener las areas destino por area origen ID") from e
            except Exception as e:
                raise DatabaseException("Error desconocido al obtener las areas destino por area origen ID") from e

