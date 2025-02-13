from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import CentroPobladoRequestDTO, CentroPobladoResponseDTO

class CentroPobladoService(ABC):
    @abstractmethod
    async def add(self, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[CentroPobladoResponseDTO]:
        pass

    @abstractmethod
    async def update(self, centro_poblado_id: int, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, centro_poblado_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[CentroPobladoResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, centro_poblado_id: int) -> CentroPobladoResponseDTO:
        pass
