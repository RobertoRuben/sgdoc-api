from abc import ABC, abstractmethod
from typing import Dict, Any
from src.dto import DerivacionRequestDTO, DerivacionResponseDTO

class DerivacionService(ABC):
    @abstractmethod
    async def add(self, derivacion_request: DerivacionRequestDTO) -> DerivacionResponseDTO:
        pass

    @abstractmethod
    async def get_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        fecha_filtro: str = None,
        estado_filtro: str = None,
        documento_id_filtro: int = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, derivacion_id: int, derivacion_request: DerivacionRequestDTO) -> DerivacionResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, derivacion_id: int) -> None:
        pass
