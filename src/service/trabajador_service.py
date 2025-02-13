from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.dto import TrabajadorRequestDTO, TrabajadorResponseDTO

class TrabajadorService(ABC):

    @abstractmethod
    async def add(self, trabajador_request: TrabajadorRequestDTO) -> TrabajadorResponseDTO:
        pass

    @abstractmethod
    async def get_all_ids_and_names(self) -> List[TrabajadorResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, trabajador_id: int, trabajador_request: TrabajadorRequestDTO) -> TrabajadorResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, trabajador_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[TrabajadorResponseDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, trabajador_id: int) -> Optional[TrabajadorResponseDTO]:
        pass
