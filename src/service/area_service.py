from abc import ABC, abstractmethod
from typing import List, Any, Dict
from src.dto.area_request_dto import AreaRequestDTO
from src.dto.area_response_dto import AreaResponseDTO

class AreaService(ABC):
    @abstractmethod
    async def add_area(self, area_request: AreaRequestDTO) -> AreaResponseDTO:
        pass

    @abstractmethod
    async def get_all_areas(self) -> List[AreaResponseDTO]:
        pass

    @abstractmethod
    async def update_area(self, area_id: int, area_request: AreaRequestDTO) -> AreaResponseDTO:
        pass

    @abstractmethod
    async def delete_area_by_id(self, area_id: int) -> None:
        pass

    @abstractmethod
    async def find_area(self, search_string: str) -> List[AreaResponseDTO]:
        pass

    @abstractmethod
    async def get_all_areas_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_area_by_id(self, area_id: int) -> AreaResponseDTO:
        pass
