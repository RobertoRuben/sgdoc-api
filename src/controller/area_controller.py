from typing import List
from fastapi import Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from src.schemas import (
    ErrorResponseSchema,
    ValidationErrorResponseSchema,
    NotAuthenticatedResponseSchema,
    DeleteSuccessfulResponseSchema
)
from src.dto import  AreaResponseDTO, AreaRequestDTO, PaginatedResponseDTO
from src.service.imp.area_service_imp import AreaServiceImpl

def get_area_service_imp(service: AreaServiceImpl = Depends()) -> AreaServiceImpl:
    return service

router = APIRouter(
    prefix="/areas",
    tags=["Areas"]
)

areas_tag_metadata = {
    "name": "Areas",
    "description": (
        "Esta sección proporciona los endpoints para gestionar la entidad de Area, incluyendo la "
        "creación, recuperación, actualización, eliminación y búsqueda de registros de areas."
    ),
}

@router.post(
    "",
    response_model=AreaResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea una nueva área en la organización"
)
async def add_area(area_request: AreaRequestDTO, service: AreaServiceImpl = Depends(get_area_service_imp)):
    return await service.add_area(area_request)


@router.get(
    "",
    response_model=List[AreaResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las áreas"
)
async def get_areas(service: AreaServiceImpl = Depends(get_area_service_imp)):
    return await service.get_all_areas()


@router.get(
    "/search",
    response_model=List[AreaResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca áreas por cadena de búsqueda"
)
async def search_areas(
    search_string: str = Query(..., description="Cadena de búsqueda para encontrar áreas"),
    service: AreaServiceImpl = Depends(get_area_service_imp)
):
    return await service.find_area(search_string)


@router.get(
    "/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene las áreas paginadas"
)
async def get_paginated_areas(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: AreaServiceImpl = Depends(get_area_service_imp)
):
    return await service.get_all_areas_paginated(page, page_size)


@router.get(
    "/{area_id}",
    response_model=AreaResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "El área no existe", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un área por su ID"
)
async def get_area_by_id(area_id: int, service: AreaServiceImpl = Depends(get_area_service_imp)):
    return await service.get_area_by_id(area_id)


@router.put(
    "/{area_id}",
    response_model=AreaResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "El área no existe", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un área"
)
async def update_area(area_id: int, area_request: AreaRequestDTO, service: AreaServiceImpl = Depends(get_area_service_imp)):
    return await service.update_area(area_id, area_request)


@router.delete(
    "/{area_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "El área no existe", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un área"
)
async def delete_area_by_id(area_id: int, service: AreaServiceImpl = Depends(get_area_service_imp)):
    await service.delete_area_by_id(area_id)
    return JSONResponse(
        content={"message": "Se eliminó el área correctamente"},
        status_code=200
    )
