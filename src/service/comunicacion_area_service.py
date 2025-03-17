from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.dto import (
    ComunicacionDestinoResponseDTO,
    ComunicacionAreaRequestDTO,
    ComunicacionAreaSimpleResponseDTO,
    ComunicacionAreaFindResponseDTO
)

class ComunicacionAreaService(ABC):
    @abstractmethod
    async def get_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_paginated_destinos_by_area_origen_id(self, area_origen_id: int) -> List[ComunicacionDestinoResponseDTO]:
        pass

    @abstractmethod
    async def add_comunicacion(self, comunicacion_area_request_dto: ComunicacionAreaRequestDTO) -> ComunicacionAreaSimpleResponseDTO:
        pass

    @abstractmethod
    async def get_by_id(self, comunicacion_area_id: int) -> ComunicacionAreaSimpleResponseDTO:
        pass

    @abstractmethod
    async def update_comunicacion(
        self,
        comunicacion_area_id: int,
        comunicacion_area_request_dto: ComunicacionAreaRequestDTO
    ) -> ComunicacionAreaSimpleResponseDTO:
        pass

    @abstractmethod
    async def delete_comunicacion(self, comunicacion_area_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[ComunicacionAreaFindResponseDTO]:
        pass
