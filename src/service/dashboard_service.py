from abc import ABC, abstractmethod
from typing import Dict, List
from src.dto import (
    IngresosPorAmbitoResponseDTO,
    IngresosPorCaserioResponseDTO,
    IngresosPorCentroPobladoResponseDTO,
    TotalIngresosResponseDTO,
    PromedioIngresosResponseDTO,
    TopIngresosResponseDTO,
    DashboardFilterRequestDTO,
)


class DashboardService(ABC):

    @abstractmethod
    async def get_total_documents_by_documentary_scope(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[IngresosPorAmbitoResponseDTO]:
        pass

    @abstractmethod
    async def get_total_documents_by_village(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[IngresosPorCaserioResponseDTO]:
        pass

    @abstractmethod
    async def get_total_documents_by_centro_poblado(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[Dict[IngresosPorCentroPobladoResponseDTO]]:
        pass

    @abstractmethod
    async def get_total_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> TotalIngresosResponseDTO:
        pass

    @abstractmethod
    async def get_average_total_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> PromedioIngresosResponseDTO:
        pass

    @abstractmethod
    async def get_top_villages_with_most_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[TopIngresosResponseDTO]:
        pass

    @abstractmethod
    async def get_top_villages_with_least_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[TopIngresosResponseDTO]:
        pass
