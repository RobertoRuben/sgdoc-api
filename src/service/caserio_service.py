from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.dto import CaserioRequestDTO, CaserioResponseDTO

class CaserioService(ABC):
    @abstractmethod
    async def add(self, caserio_request: CaserioRequestDTO) -> CaserioResponseDTO:
        pass

    @abstractmethod
    async def get_names(self) -> List[CaserioResponseDTO]:
        pass

    @abstractmethod
    async def update(self, caserio_id: int, caserio_request: CaserioRequestDTO) -> CaserioResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, caserio_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_by_centro_poblado_id(self, centro_poblado_id: Optional[int]) -> List[CaserioResponseDTO]:
        pass

    @abstractmethod
    async def find(self, search_string: str) -> List[CaserioResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, caserio_id: int) -> Optional[CaserioResponseDTO]:
        pass
