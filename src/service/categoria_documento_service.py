from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto.categoria_documento_request_dto import CategoriaDocumentoRequestDTO
from src.dto.categoria_documento_response_dto import CategoriaDocumentoResponseDTO

class CategoriaDocumentoService(ABC):
    @abstractmethod
    async def add_categoria_documento(self, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        pass

    @abstractmethod
    async def get_all_categorias_documento(self) -> List[CategoriaDocumentoResponseDTO]:
        pass

    @abstractmethod
    async def update_categoria_documento(self, categoria_id: int, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        pass

    @abstractmethod
    async def delete_categoria_documento_by_id(self, categoria_id: int) -> None:
        pass

    @abstractmethod
    async def find_categoria_documento(self, nombre_categoria: str) -> List[CategoriaDocumentoResponseDTO]:
        pass

    @abstractmethod
    async def get_categorias_documento_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_categoria_documento_by_id(self, categoria_id: int) -> CategoriaDocumentoResponseDTO:
        pass
