from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import AmbitoRequestDTO, AmbitoResponseDTO

class AmbitoService(ABC):

    @abstractmethod
    async def add(self, ambito_request: AmbitoRequestDTO) -> AmbitoResponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[AmbitoResponseDTO]:
        pass

    @abstractmethod
    async def update(self, ambito_id: int, ambito_request: AmbitoRequestDTO) -> AmbitoResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, ambito_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[AmbitoResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, ambito_id: int) -> AmbitoResponseDTO:
        pass
