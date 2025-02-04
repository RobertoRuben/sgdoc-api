from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.service.remitente_service import RemitenteService
from src.dto.remitente_request import RemitenteRequest
from src.dto.remitente_response import RemitenteResponse
from src.dto.pagination_response import PaginatedResponse

router = APIRouter(tags=["Remitentes"])

remitentes_tag_metadata={
    "name": "Remitentes",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Remitente, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Remitente. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post(
    "/remitentes",
    response_model=RemitenteResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo remitente"
)
async def add_remitente(remitente_request: RemitenteRequest, service: RemitenteService = Depends()):
    return service.add_remitente(remitente_request)


@router.get(
    "/remitentes",
    response_model=List[RemitenteResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los remitentes"
)
async def get_remitentes(remitente_service: RemitenteService = Depends()):
    return remitente_service.get_remitentes()


@router.get(
    "/remitentes/search",
    response_model=List[RemitenteResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca remitentes por cadena de búsqueda"
)
async def search_remitentes(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar remitentes"),
    remitente_service: RemitenteService = Depends()
):
    return remitente_service.find_remitentes_by_string(search_string)


@router.get(
    "/remitentes/paginated",
    response_model=PaginatedResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la lista de remitentes paginada"
)
async def get_remitentes(page: int = 1, page_size: int = 10, remitente_service: RemitenteService = Depends()):
    return remitente_service.get_remitentes_with_pagination(page, page_size)


@router.get(
    "/remitentes/{remitente_id}",
    response_model=RemitenteResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un remitente por ID"
)
async def get_remitente_by_id(remitente_id: int, remitente_service: RemitenteService = Depends()):
    return remitente_service.get_remitente_by_id(remitente_id)


@router.put(
    "/remitentes/{remitente_id}",
    response_model=RemitenteResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un remitente"
)
async def update_remitente(remitente_id: int, remitente_request: RemitenteRequest, remitente_service: RemitenteService = Depends()):
    return remitente_service.update_remitente(remitente_id, remitente_request)


@router.delete(
    "/remitentes/{remitente_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un remitente"
)
async def delete_remitente(remitente_id: int, remitente_service: RemitenteService = Depends()):
    remitente_service.delete_remitente(remitente_id)
    return JSONResponse(content={"message": "Se eliminó el remitente correctamente"}, status_code=200)






