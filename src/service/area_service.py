from abc import ABC, abstractmethod
from typing import List, Any, Dict
from src.dto import AreaRequestDTO, AreaResponseDTO

class AreaService(ABC):
    @abstractmethod
    async def add(self, area_request: AreaRequestDTO) -> AreaResponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[AreaResponseDTO]:
        pass

    @abstractmethod
    async def update(self, area_id: int, area_request: AreaRequestDTO) -> AreaResponseDTO:
        pass

    @abstractmethod
    async def delete(self, area_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[AreaResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, area_id: int) -> AreaResponseDTO:
        pass
