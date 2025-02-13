from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.dto import ComunicacionDestinoResponseDTO

class ComunicacionAreaService(ABC):
    @abstractmethod
    async def get_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_paginated_destinos_by_area_origen_id(self, area_origen_id: int) -> List[ComunicacionDestinoResponseDTO]:
        pass
