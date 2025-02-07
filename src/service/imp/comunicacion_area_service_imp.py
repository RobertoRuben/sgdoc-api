from typing import List, Dict, Any
from fastapi import Depends
from src.dto import ComunicacionDestinoResponseDTO
from src.repository import ComunicacionAreaRepository
from src.service import ComunicacionAreaService


class ComunicacionAreaServiceImp(ComunicacionAreaService):
    def __init__(self, comunicacion_area_repository: ComunicacionAreaRepository = Depends()):
        self.comunicacion_area_repository = comunicacion_area_repository


    async def get_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        return await self.comunicacion_area_repository.get_all_paginated(page, page_size)


    async def get_paginated_destinos_by_area_origen_id(self, area_origen_id: int) -> List[ComunicacionDestinoResponseDTO]:
        areas_destinos = await self.comunicacion_area_repository.get_areas_destino_by_area_origen_id(area_origen_id)
        return [
            ComunicacionDestinoResponseDTO(
                area_destino_id=area_destino["area_destino_id"],
                nombre_area_destino=area_destino["nombre_area"]
            ) for area_destino in areas_destinos
        ]
