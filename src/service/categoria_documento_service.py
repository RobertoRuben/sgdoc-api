from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.dto import CategoriaDocumentoRequestDTO, CategoriaDocumentoResponseDTO

class CategoriaDocumentoService(ABC):
    @abstractmethod
    async def add(self, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[CategoriaDocumentoResponseDTO]:
        pass

    @abstractmethod
    async def update(self, categoria_id: int, categoria_request: CategoriaDocumentoRequestDTO) -> CategoriaDocumentoResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, categoria_id: int) -> None:
        pass

    @abstractmethod
    async def find(self, nombre_categoria: str) -> List[CategoriaDocumentoResponseDTO]:
        pass

    @abstractmethod
    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, categoria_id: int) -> CategoriaDocumentoResponseDTO:
        pass
