from typing import List
from fastapi import APIRouter, Depends
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto import (
    DocumentosIngresadosResponseDTO,
    TotalDocumentosDerivaodsResponseDTO,
    TotalDocumentosNoDerivadosResponseDTO,
    TotalDocumentosPorCaserioResponseDTO
)
from src.service import DashboardMesaPartesService
from src.service.imp import DashboardMesaPartesServiceImp

router = APIRouter(
    prefix="/dashboard-mesa-partes",
    tags=["Documentos por fecha actual"]
)

documentos_by_current_date_tag_metadata = {
    "name": "Documentos por fecha actual",
    "description": "Esta sección proporciona los endpoints para obtener la cantidad de documentos, documentos derivados "
                   "y documentos pendientes de derivar en la fecha actual.",
}


def get_dashboard_mesa_partes_service_imp(service: DashboardMesaPartesServiceImp = Depends()) -> DashboardMesaPartesService:
    return service


@router.get(
    "/documents/received-today",
    response_model=DocumentosIngresadosResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos ingresados en la fecha actual"
)
async def get_todays_received_documents(
    service: DashboardMesaPartesService = Depends(get_dashboard_mesa_partes_service_imp)
):
    return await service.get_todays_total_documents_received()


@router.get(
    "/documents/derived-today",
    response_model=TotalDocumentosDerivaodsResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos derivados en la fecha actual"
)
async def get_todays_derived_documents(
    service: DashboardMesaPartesService = Depends(get_dashboard_mesa_partes_service_imp)
):
    return await service.get_todays_total_derived_documents()


@router.get(
    "/documents/pending-derivation-today",
    response_model=TotalDocumentosNoDerivadosResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos pendientes de derivar en la fecha actual"
)
async def get_todays_pending_derivation_documents(
    service: DashboardMesaPartesService = Depends(get_dashboard_mesa_partes_service_imp)
):
    return await service.get_todays_total_pending_derived_documents()


@router.get(
    "/documents/received-today/by-village",
    response_model=List[TotalDocumentosPorCaserioResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos ingresados en la fecha actual, agrupados por caserío"
)
async def get_todays_received_documents_by_village(
    service: DashboardMesaPartesService = Depends(get_dashboard_mesa_partes_service_imp)
):
    return await service.get_todays_documents_by_village()