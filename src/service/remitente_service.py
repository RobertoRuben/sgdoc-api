from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import RemitenteRequestDTO, RemitenteResponseDTO

class RemitenteService(ABC):

    @abstractmethod
    async def add(self, remitente_request: RemitenteRequestDTO) -> RemitenteResponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[RemitenteResponseDTO]:
        pass

    @abstractmethod
    async def update(self, remitente_id: int, remitente_request: RemitenteRequestDTO) -> RemitenteResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, remitente_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[RemitenteResponseDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, remitente_id: int) -> RemitenteResponseDTO:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass
