from typing import List, Dict, Any
from fastapi import  Depends
from src.dto.comunicacion_destino_response import ComunicacionDestinoResponse
from src.repository.comunicacion_area_repository import ComunicacionAreaRepository

class ComunicacionAreaService:
    def __init__(self, comunicacion_area_repository: ComunicacionAreaRepository = Depends()):
        self.comunicacion_area_repository = comunicacion_area_repository

    def get_all(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        return self.comunicacion_area_repository.get_all_paginated(page, page_size)

    def get_areas_destino_by_area_origen_id(self, area_origen_id: int) -> List[ComunicacionDestinoResponse]:
        areas_destino = self.comunicacion_area_repository.get_areas_destino_by_area_origen_id(area_origen_id)

        return [
            ComunicacionDestinoResponse(
                area_destino_id=area_destino["area_destino_id"],
                nombre_area_destino=area_destino["nombre_area"]
            ) for area_destino in areas_destino
        ]