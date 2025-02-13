from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    DocumentosIngresadosResponseDTO,
    TotalDocumentosDerivadosResponseDTO,
    TotalDocumentosNoDerivadosResponseDTO,
    TotalDocumentosPorCaserioResponseDTO,
)

class DashboardMesaPartesService(ABC):
    @abstractmethod
    async def get_todays_total_documents_received(self) -> DocumentosIngresadosResponseDTO:
        pass

    @abstractmethod
    async def get_todays_total_derived_documents(self) -> TotalDocumentosDerivadosResponseDTO:
        pass

    @abstractmethod
    async def get_todays_total_pending_derived_documents(self) -> TotalDocumentosNoDerivadosResponseDTO:
        pass

    @abstractmethod
    async def get_todays_documents_by_village(self) -> List[TotalDocumentosPorCaserioResponseDTO]:
        pass
