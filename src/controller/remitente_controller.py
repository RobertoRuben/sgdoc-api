from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto import RemitenteRequestDTO, RemitenteResponseDTO, PaginatedResponseDTO
from src.service import RemitenteService
from src.service.imp import RemitenteServiceImp

router = APIRouter(
    prefix="/remitentes",
    tags=["Remitentes"]
)

remitentes_tag_metadata={
    "name": "Remitentes",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Remitente, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Remitente. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

def get_remitentes_imp(service: RemitenteServiceImp = Depends()) -> RemitenteService:
    return service

@router.post(
    "",
    response_model=RemitenteResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo remitente"
)
async def add_remitente(remitente_request: RemitenteRequestDTO, service: RemitenteService = Depends(get_remitentes_imp)):
    return await service.add(remitente_request)


@router.get(
    "",
    response_model=List[RemitenteResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los remitentes"
)
async def get_all_remitentes(service: RemitenteService = Depends(get_remitentes_imp)):
    return await service.get_all()


@router.get(
    "/search",
    response_model=List[RemitenteResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca remitentes por cadena de búsqueda"
)
async def search_remitentes(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar remitentes"),
    service: RemitenteService = Depends(get_remitentes_imp)
):
    return await service.find(search_string)


@router.get(
    "/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene la lista de remitentes paginada"
)
async def get_paginated_remitentes(
    page: int = 1,
    page_size: int = 10,
    service: RemitenteService = Depends(get_remitentes_imp)
):
    return await service.get_paginated(page, page_size)


@router.get(
    "/{remitente_id}",
    response_model=RemitenteResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un remitente por ID"
)
async def get_remitente_by_id(
    remitente_id: int,
    service: RemitenteService = Depends(get_remitentes_imp)
):
    return await service.get_by_id(remitente_id)


@router.put(
    "/{remitente_id}",
    response_model=RemitenteResponseDTO,
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
async def update_remitente(
    remitente_id: int,
    remitente_request: RemitenteRequestDTO,
    service: RemitenteService = Depends(get_remitentes_imp)
):
    return service.update(remitente_id, remitente_request)


@router.delete(
    "/{remitente_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un remitente"
)
async def delete_remitente_by_id(
    remitente_id: int,
    service: RemitenteService = Depends(get_remitentes_imp)
):
    await service.delete_by_id(remitente_id)
    return JSONResponse(
        content={"message": "Se eliminó el remitente correctamente"},
        status_code=200
    )






