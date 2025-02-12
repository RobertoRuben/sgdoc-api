from typing import List
from fastapi import Depends
from src.dto import (
    IngresosPorAmbitoResponseDTO,
    IngresosPorCaserioResponseDTO,
    IngresosPorCentroPobladoResponseDTO,
    TotalIngresosResponseDTO,
    PromedioIngresosResponseDTO,
    TopIngresosResponseDTO,
    DashboardFilterRequestDTO,
)
from src.repository import DashboardRepository
from src.service import DashboardService
from src.exception import InternalServerException


class DashboardServiceImp(DashboardService):
    def __init__(self, dashboard_repository: DashboardRepository = Depends()):
        self.dashboard_repository = dashboard_repository

    async def get_total_documents_by_documentary_scope(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[IngresosPorAmbitoResponseDTO]:
        try:
            results = await self.dashboard_repository.get_total_documents_by_documentary_scope(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return [
                IngresosPorAmbitoResponseDTO(
                    ambito=result["ambito"],
                    total=result["total"],
                )
                for result in results
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e


    async def get_total_documents_by_village(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[IngresosPorCaserioResponseDTO]:
        try:
            results = await self.dashboard_repository.get_total_documents_by_village(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return [
                IngresosPorCaserioResponseDTO(
                    caserio=result["caserio"],
                    total_documentos=result["total_documentos"],
                )
                for result in results
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e


    async def get_total_documents_by_centro_poblado(
            self,
            dashboard_request: DashboardFilterRequestDTO
    ) -> List[IngresosPorCentroPobladoResponseDTO]:
        try:
            results = await self.dashboard_repository.get_total_documents_by_centro_poblado(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            response = [
                IngresosPorCentroPobladoResponseDTO(
                    mes=item["mes"],
                    centros=item.get("centros", [])
                )
                for item in results
            ]

            return response

        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por centro poblado",
                error_details=str(e)
            ) from e


    async def get_total_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> TotalIngresosResponseDTO:
        try:
            total_documents = await self.dashboard_repository.get_total_documents(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return TotalIngresosResponseDTO(
                total_documentos=total_documents
            )
        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e


    async def get_average_total_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> PromedioIngresosResponseDTO:
        try:
            average_total_documents = await self.dashboard_repository.get_average_total_documents(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return PromedioIngresosResponseDTO(
                promedio_ingresos=average_total_documents
            )
        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e


    async def get_top_villages_with_most_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[TopIngresosResponseDTO]:
        try:
            results = await self.dashboard_repository.get_top_villages_with_most_documents(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return [
                TopIngresosResponseDTO(
                    caserio=result["caserio"],
                    total_documentos=result["total_documentos"],
                )
                for result in results
            ]

        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e


    async def get_top_villages_with_least_documents(
        self,
        dashboard_request: DashboardFilterRequestDTO
    ) -> List[TopIngresosResponseDTO]:
        try:
            results = await self.dashboard_repository.get_top_villages_with_least_documents(
                p_start_year=dashboard_request.start_year,
                p_end_year=dashboard_request.end_year,
                p_end_month=dashboard_request.end_month,
                p_start_month=dashboard_request.start_month,
            )

            return [
                TopIngresosResponseDTO(
                    caserio=result["caserio"],
                    total_documentos=result["total_documentos"],
                )
                for result in results
            ]

        except Exception as e:
            raise InternalServerException(
                detail="Ocurrió un error al obtener el total de documentos por ámbito",
                error_details=str(e)
            ) from e
