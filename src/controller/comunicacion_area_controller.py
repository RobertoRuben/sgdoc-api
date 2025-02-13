from typing import List
from fastapi import APIRouter, Depends
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto import PaginatedResponseDTO, ComunicacionDestinoResponseDTO
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