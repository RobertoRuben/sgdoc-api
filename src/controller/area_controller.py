from typing import List
from fastapi import Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from src.schemas import ErrorResponse, ValidationErrorResponse, NotAuthenticatedResponse
from src.dto.area_response import AreaResponse
from src.dto.area_request import AreaRequest
from src.dto.pagination_response import PaginatedResponse
from src.service.areas_service import AreaService

router = APIRouter(tags=["Areas"])

areas_tag_metadata = {
    "name": "Areas",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Area, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de areas.",
}

@router.post(
    "/areas",
    response_model=AreaResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponse},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponse},
        422: {"description": "Error de validación", "model": ValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Crea una nueva área en la organización"
)
async def add_area(area_request: AreaRequest, service: AreaService = Depends()):
    return service.add_area(area_request)


@router.get(
    "/areas",
    response_model=List[AreaResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Obtiene todas las áreas"
)
async def get_areas(service: AreaService = Depends()):
    return service.get_all_areas()


@router.get(
    "/areas/search",
    response_model=List[AreaResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Busca áreas por cadena de búsqueda"
)
async def search_areas(
    search_string: str = Query(..., description="Cadena de búsqueda para encontrar áreas"),
    service: AreaService = Depends()
):
    return service.find_areas_by_string(search_string)


@router.get(
    "/areas/paginated",
    response_model=PaginatedResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Obtiene las áreas paginadas"
)
async def get_paginated_areas(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: AreaService = Depends()
):
    return service.get_all_areas_by_pagination(page, page_size)


@router.get(
    "/areas/{area_id}",
    response_model=AreaResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        404: {"description": "El área no existe", "model": ErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Obtiene un área por su ID"
)
async def get_area_by_id(area_id: int, service: AreaService = Depends()):
    return service.get_area_by_id(area_id)


@router.put(
    "/areas/{area_id}",
    response_model=AreaResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        404: {"description": "El área no existe", "model": ErrorResponse},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponse},
        422: {"description": "Error de validación", "model": ValidationErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Actualiza un área"
)
async def update_area(area_id: int, area_request: AreaRequest, service: AreaService = Depends()):
    return service.update_area(area_id, area_request)


@router.delete(
    "/areas/{area_id}",
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponse},
        404: {"description": "El área no existe", "model": ErrorResponse},
        500: {"description": "Error interno del servidor", "model": ErrorResponse},
    },
    description="Elimina un área"
)
async def delete_area_by_id(area_id: int, service: AreaService = Depends()):
    service.delete_area_by_id(area_id)
    return JSONResponse(content={"message": "Se eliminó el área correctamente"}, status_code=200)
