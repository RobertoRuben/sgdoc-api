from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import RolRequestDTO, RolReponseDTO

class RolService(ABC):
    @abstractmethod
    async def add(self, rol_request: RolRequestDTO) -> RolReponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[RolReponseDTO]:
        pass

    @abstractmethod
    async def update(self, rol_id: int, rol_request: RolRequestDTO) -> RolReponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, rol_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[RolReponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, rol_id: int) -> RolReponseDTO:
        pass
