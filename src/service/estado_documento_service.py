from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import EstadoDocumentoRequestDTO, EstadoDocumentoResponseDTO


class EstadoDocumentoService(ABC):

    @abstractmethod
    async def add(self, estado_documento_request: EstadoDocumentoRequestDTO) -> EstadoDocumentoResponseDTO:
        pass

    @abstractmethod
    async def get_all(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, estado_documento_id: int, estado_documento_request: EstadoDocumentoRequestDTO) -> EstadoDocumentoResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, estado_documento_id: int) -> None:
        pass

    @abstractmethod
    async def get_all_by_documento_id(self, documento_id: int) -> List[EstadoDocumentoResponseDTO]:
        pass
