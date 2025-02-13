from typing import List
from fastapi import APIRouter, Depends
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto import (
    IngresosPorAmbitoResponseDTO,
    IngresosPorCaserioResponseDTO,
    IngresosPorCentroPobladoResponseDTO,
    TotalIngresosResponseDTO,
    PromedioIngresosResponseDTO,
    TopIngresosResponseDTO,
    DashboardFilterRequestDTO,
)
from src.service import DashboardService
from src.service.imp import DashboardServiceImp

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

dashboard_tag_metadata = {
    "name": "Dashboard",
    "description": "Esta sección proporciona los endpoints para obtener los ingresos por ámbito, caserío, centro poblado, "
                   "total de ingresos, promedio de ingresos y los top ingresos."
}

def get_dahsboard_service_imp(service: DashboardServiceImp = Depends()) -> DashboardService:
    return service


@router.post(
    "/documentary-scope/total",
    response_model=List[IngresosPorAmbitoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el total de documentos agrupados por ámbito documental."
)
async def get_total_documents_by_documentary_scope(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_total_documents_by_documentary_scope(dashboard_request)


@router.post(
    "/village/total",
    response_model=List[IngresosPorCaserioResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el total de documentos agrupados por caserío."
)
async def get_total_documents_by_village(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_total_documents_by_village(dashboard_request)


@router.post(
    "/centro-poblado/total",
    response_model=List[IngresosPorCentroPobladoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el total de documentos agrupados por centro poblado."
)
async def get_total_documents_by_centro_poblado(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_total_documents_by_centro_poblado(dashboard_request)


@router.post(
    "/documents/total",
    response_model=TotalIngresosResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el total de documentos en el rango dado."
)
async def get_total_documents(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_total_documents(dashboard_request)


@router.post(
    "/documents/average",
    response_model=PromedioIngresosResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el promedio de documentos en el rango dado."
)
async def get_average_total_documents(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_average_total_documents(dashboard_request)


@router.post(
    "/top-villages/most",
    response_model=List[TopIngresosResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el top de caseríos con más documentos en el rango dado."
)
async def get_top_villages_with_most_documents(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_top_villages_with_most_documents(dashboard_request)


@router.post(
    "/top-villages/least",
    response_model=List[TopIngresosResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el top de caseríos con menos documentos en el rango dado."
)
async def get_top_villages_with_least_documents(
    dashboard_request: DashboardFilterRequestDTO,
    service: DashboardService = Depends(get_dahsboard_service_imp),
):
    return await service.get_top_villages_with_least_documents(dashboard_request)


