from typing import List
from fastapi import APIRouter, Depends
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto.comunicacion_destino_response import ComunicacionDestinoResponse
from src.dto.paginated_response import PaginatedResponseDTO
from src.service.imp.comunicacion_area_service_imp import ComunicacionAreaServiceImp

router = APIRouter(tags=["Comunicaciones entre Áreas"])

comunicaciones_area_tag_metadata={
    "name": "Comunicaciones entre Áreas",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Comunicación entre Áreas, "
                   "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros de Comunicación entre Áreas.",
}

@router.get(
    "/comunicaciones-area",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las comunicaciones entre áreas"
)
async def get_all_comunicaciones_area(page: int = 1, page_size: int = 10, service: ComunicacionAreaServiceImp = Depends()):
    return service.get_all(page, page_size)


@router.get(
    "/comunicaciones-area/{area_origen_id}/destinos",
    response_model=List[ComunicacionDestinoResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene las áreas destino por ID de área de origen"
)
async def get_areas_destino_by_area_origen_id(area_origen_id: int, service: ComunicacionAreaServiceImp = Depends()
):
    return service.get_areas_destino_by_area_origen_id(area_origen_id)