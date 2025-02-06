from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.dto.ambito_request import AmbitoRequest
from src.dto.ambito_response import AmbitoResponse
from src.dto.pagination_response import PaginatedResponse
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema
from src.service.ambito_service import AmbitoService

router = APIRouter(tags=["Ambitos"])

ambitos_tag_metadata = {
    "name": "Ambitos",
    "description": (
        "Esta sección proporciona los endpoints para gestionar la entidad de Ambito, "
        "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros "
        "de ambitos documentales."
    ),
}

@router.post(
    "/ambitos",
    response_model=AmbitoResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo ambito documental"
)
async def add_ambito(ambito_request: AmbitoRequest, service: AmbitoService = Depends()):
    return service.add_ambito(ambito_request)


@router.get(
    "/ambitos",
    response_model=List[AmbitoResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los ambitos documentales"
)
async def get_ambitos(service: AmbitoService = Depends()):
    return service.get_all_ambitos()


@router.get(
    "/ambitos/paginated",
    response_model=PaginatedResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los ambitos documentales paginados"
)
async def get_paginated_ambitos(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: AmbitoService = Depends()
):
    return service.get_ambitos_paginated(page, page_size)


@router.get(
    "/ambitos/search",
    response_model=List[AmbitoResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca ambitos documentales por cadena de búsqueda"
)
async def search_ambitos(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar ambitos documentales"),
    service: AmbitoService = Depends()
):
    return service.find_ambito(search_string)


@router.put(
    "/ambitos/{ambito_id}",
    response_model=AmbitoResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Ambito no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un ambito documental"
)
async def update_ambito(ambito_id: int, ambito_request: AmbitoRequest, service: AmbitoService = Depends()):
    return service.update_ambito(ambito_id, ambito_request)


@router.delete(
    "/ambitos/{ambito_id}", response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Ambito no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un ambito documental"
)
async def delete_ambito(ambito_id: int, service: AmbitoService = Depends()):
    service.delete_ambito(ambito_id)
    return JSONResponse(content={"message": "Se eliminó el ambito documental correctamente"}, status_code=200)


@router.get(
    "/ambitos/{ambito_id}",
    response_model=AmbitoResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Ambito no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un ambito documental por su ID"
)
async def get_ambito_by_id(ambito_id: int, service: AmbitoService = Depends()):
    return service.get_ambitos_by_id(ambito_id)
