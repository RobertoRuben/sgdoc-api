from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.dto import AmbitoRequestDTO, AmbitoResponseDTO, PaginatedResponseDTO
from src.schemas import *
from src.service.imp import AmbitoServiceImp
from src.service import AmbitoService

def get_ambito_service_imp(service: AmbitoServiceImp = Depends()) -> AmbitoService:
    return service


router = APIRouter(
    prefix="/ambitos",
    tags=["Ambitos"]
)

ambitos_tag_metadata = {
    "name": "Ambitos",
    "description": (
        "Esta sección proporciona los endpoints para gestionar la entidad de Ambito Documental, incluyendo la "
        "creación, recuperación, actualización, eliminación y búsqueda de registros de ambitos documentales."
    ),
}

@router.post(
    "",
    response_model=AmbitoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo ambito documental"
)
async def add_ambito(ambito_request: AmbitoRequestDTO, service: AmbitoService = Depends(get_ambito_service_imp)):
    return await service.add_ambito(ambito_request)


@router.get(
    "",
    response_model=List[AmbitoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los ambitos documentales"
)
async def get_ambitos(service: AmbitoService = Depends(get_ambito_service_imp)):
    return await service.get_all_ambitos()


@router.get(
    "/paginated",
    response_model=PaginatedResponseDTO,
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
    service: AmbitoService = Depends(get_ambito_service_imp)
):
    return await service.get_ambitos_paginated(page, page_size)


@router.get(
    "/search",
    response_model=List[AmbitoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca ambitos documentales por cadena de búsqueda"
)
async def search_ambitos(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar ambitos documentales"),
    service: AmbitoService = Depends(get_ambito_service_imp)
):
    return await service.find_ambito(search_string)


@router.put(
    "/{ambito_id}",
    response_model=AmbitoResponseDTO,
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
async def update_ambito(ambito_id: int, ambito_request: AmbitoRequestDTO, service: AmbitoService = Depends(get_ambito_service_imp)):
    return await service.update_ambito(ambito_id, ambito_request)


@router.delete(
    "/{ambito_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Ambito no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un ambito documental"
)
async def delete_ambito_by_id(ambito_id: int, service: AmbitoService = Depends(get_ambito_service_imp)):
    await service.delete_ambito(ambito_id)
    return JSONResponse(
        content={"message": "Se eliminó el ambito documental correctamente"},
        status_code=200
    )


@router.get(
    "/{ambito_id}",
    response_model=AmbitoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Ambito no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un ambito documental por su ID"
)
async def get_ambito_by_id(ambito_id: int, service: AmbitoService = Depends(get_ambito_service_imp)):
    return await service.get_ambito_by_id(ambito_id)
