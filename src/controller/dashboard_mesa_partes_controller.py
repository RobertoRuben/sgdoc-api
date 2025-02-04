from typing import List
from  fastapi import APIRouter, Depends
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto.documentos_by_current_date_response import *
from src.service.mesa_partes_dashboard_service import DashboardMesaPartesService

router = APIRouter(tags=["Documentos por fecha actual"])

documentos_by_current_date_tag_metadata={
    "name": "Documentos por fecha actual",
    "description": "Esta sección proporciona los endpoints para obtener la cantidad de documentos, documentos derivados"
                   " y documentos pendientes de derivar en la fecha actual.",
}


@router.get(
    "/documentos-by-current-date",
    response_model=DocumentosByCurrentDateResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos ingresados en la fecha actual"
)
async def get_total_number_documents_today(service: DashboardMesaPartesService = Depends()):
    return service.get_total_number_documents_today()


@router.get(
    "/documentos-by-current-date/derived",
    response_model=TotalDerivedDocumentsToday,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos derivados en la fecha actual"
)
async def get_total_number_derived_documents_today(service: DashboardMesaPartesService = Depends()):
    return service.get_total_number_derived_documents_today()


@router.get(
    "/documentos-by-current-date/pending-derived",
    response_model=TotalPendingDerivedDocumentsToday,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos pendientes de derivar en la fecha actual"
)
async def get_total_number_pending_derived_documents_today(service: DashboardMesaPartesService = Depends()):
    return service.get_total_number_pending_derived_documents_today()


@router.get(
    "/documentos-by-current-date/caserios",
    response_model=List[TotalDocumentsByCaserioToday],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la cantidad de documentos ingresados en la fecha actual por caserío"
)
async def get_total_documents_by_caserio_today(service: DashboardMesaPartesService = Depends()):
    return service.get_total_documents_by_caserio_today()