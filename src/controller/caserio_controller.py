from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.dto.caserio_request_dto import CaserioRequestDTO
from src.dto.caserio_response_dto import CaserioResponseDTO, CaserioResponseWithCentroPobladoId, CaserioSimpleResponse
from src.dto.paginated_response import PaginatedResponseDTO
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema
from src.service.caserio_service import CaserioService

router = APIRouter(tags=["Caserios"])

caserios_tag_metadata = {
    "name": "Caserios",
    "description": (
        "Esta sección proporciona los endpoints para gestionar la entidad de Caserio, "
        "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros "
        "de caserios."
    ),
}

@router.post(
    "/caserios",
    response_model=CaserioResponseWithCentroPobladoId,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El caserio ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo caserio"
)
async def add_caserio(caserio_request: CaserioRequestDTO, service: CaserioService = Depends()):
    return service.add_caserio(caserio_request)


@router.get(
    "/caserios",
    response_model=List[CaserioResponseWithCentroPobladoId],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los caserios, filtrados por centro poblado si se proporciona un ID"
)
async def get_caserios_by_centro_poblado_id(
    centro_poblado_id: int | None = Query(None, description="ID del centro poblado para filtrar caserios"),
    service: CaserioService = Depends()
):
    return service.get_all_caserios_by_centro_poblado_id(centro_poblado_id)


@router.get(
    "/caserios/names",
    response_model=List[CaserioSimpleResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los nombres de todos los caserios"
)
async def get_caserios_names(service: CaserioService = Depends()):
    return service.get_caserios_names()


@router.get(
    "/caserios/search",
    response_model=List[CaserioResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "No se encontraron caserios", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca caserios por nombre"
)
async def search_caserios_by_name(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar caserios"),
    service: CaserioService = Depends()
):
    return service.find_by_string(search_string)


@router.get(
    "/caserios/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los caserios paginados"
)
async def get_paginated_caserios(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: CaserioService = Depends()
):
    return service.get_all_caserios_by_pagination(page, page_size)


@router.get(
    "/caserios/{caserio_id}",
    response_model=CaserioResponseWithCentroPobladoId,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Caserio no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un caserio por su ID"
)
async def get_caserio_by_id(caserio_id: int, service: CaserioService = Depends()):
    return service.get_caserio_by_id(caserio_id)


@router.put(
    "/caserios/{caserio_id}",
    response_model=CaserioResponseWithCentroPobladoId,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Caserio no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un caserio"
)
async def update_caserio(caserio_id: int, caserio_request: CaserioRequestDTO, service: CaserioService = Depends()):
    return service.update_caserio(caserio_id, caserio_request)


@router.delete(
    "/caserios/{caserio_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Caserio no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un caserio"
)
async def delete_caserio_by_id(caserio_id: int, service: CaserioService = Depends()):
    service.delete_caserio_by_id(caserio_id)
    return JSONResponse(content={"message": "Se eliminó el caserio correctamente"}, status_code=200)