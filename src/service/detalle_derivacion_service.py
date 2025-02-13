from abc import ABC, abstractmethod
from typing import List
from src.dto import DetalleDerivacionRequestDTO, DetalleDerivacionResponseDTO


class DetalleDerivacionService(ABC):
    @abstractmethod
    async def add(self, derivacion_request: DetalleDerivacionRequestDTO) -> DetalleDerivacionResponseDTO:
        pass

    @abstractmethod
    async def get_paginated_by_id(self, derivacion_id: int) -> List[DetalleDerivacionResponseDTO]:
        pass

    @abstractmethod
    async def update(
        self,
        detalle_derivacion_id: int,
        detalle_derivacion_request: DetalleDerivacionRequestDTO
    ) -> DetalleDerivacionResponseDTO:
        pass

    @abstractmethod
    async def delete_by_id(self, detalle_derivacion_id: int) -> None:
        pass
