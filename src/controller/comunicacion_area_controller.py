from typing import List
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto import (
    PaginatedResponseDTO,
    ComunicacionAreaRequestDTO ,
    ComunicacionDestinoResponseDTO,
    ComunicacionAreaSimpleResponseDTO,
    ComunicacionAreaFindResponseDTO
)
from src.service import ComunicacionAreaService
from src.service.imp import ComunicacionAreaServiceImp

def get_comunicacion_areas_imp(service: ComunicacionAreaServiceImp = Depends()) -> ComunicacionAreaService:
    return service

router = APIRouter(
    prefix="/comunicaciones-area",
    tags=["Comunicaciones entre Áreas"]
)

comunicaciones_area_tag_metadata={
    "name": "Comunicaciones entre Áreas",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Comunicación entre Áreas, "
                   "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros de Comunicación entre Áreas.",
}

@router.get(
    "",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las comunicaciones entre áreas"
)
async def get_paginated_comunicaciones_area(
    page: int = 1,
    page_size: int = 10,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.get_paginated(page, page_size)


@router.post(
    "",
    response_model=ComunicacionAreaSimpleResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Agrega una nueva comunicación entre áreas"
)
async def add_comunicacion_area(
    comunicacion_area_request_dto: ComunicacionAreaRequestDTO,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.add_comunicacion(comunicacion_area_request_dto)


@router.get(
    "/search",
    response_model=List[ComunicacionAreaFindResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca comunicaciones entre áreas por cadena de búsqueda"
)
async def find_comunicacion_area(
    search_string: str,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.find(search_string)


@router.get(
    "/{comunicacion_area_id}",
    response_model=ComunicacionAreaSimpleResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene una comunicación entre áreas por ID"
)
async def get_comunicacion_area_by_id(
    comunicacion_area_id: int,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.get_by_id(comunicacion_area_id)


@router.get(
    "/{area_origen_id}/destinos",
    response_model=List[ComunicacionDestinoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene las áreas destino por ID de área de origen"
)
async def get_paginated_areas_destino_by_area_origen_id(
    area_origen_id: int,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.get_paginated_destinos_by_area_origen_id(area_origen_id)


@router.put(
    "/{comunicacion_area_id}",
    response_model=ComunicacionAreaSimpleResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza una comunicación entre áreas por ID"
)
async def update_comunicacion_area(
    comunicacion_area_id: int,
    comunicacion_area_request_dto: ComunicacionAreaRequestDTO,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    return await service.update_comunicacion(comunicacion_area_id, comunicacion_area_request_dto)


@router.delete(
    "/{comunicacion_area_id}",
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina una comunicación entre áreas por ID"
)
async def delete_comunicacion_area(
    comunicacion_area_id: int,
    service: ComunicacionAreaService = Depends(get_comunicacion_areas_imp)
):
    await service.delete_comunicacion(comunicacion_area_id)
    return JSONResponse(
        content={"message": "Se eliminó la comunicacion correctamente"},
        status_code=200
    )


