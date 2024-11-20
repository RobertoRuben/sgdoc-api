from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from src.dto.comunicacion_destino_response import ComunicacionDestinoResponse
from src.dto.pagination_response import PaginatedResponse
from src.service.comunicacion_area_service import ComunicacionAreaService

router = APIRouter(tags=["Comunicaciones entre Áreas"])

comunicaciones_area_tag_metadata={
    "name": "Comunicaciones entre Áreas",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Comunicación entre Áreas, "
                   "incluyendo la creación, recuperación, actualización, eliminación y búsqueda de registros de Comunicación entre Áreas.",
}

@router.get("/comunicaciones_area", response_model=PaginatedResponse, description="Obtiene todas las comunicaciones entre áreas")
async def get_all_comunicaciones_area(page: int = 1, page_size: int = 10, service: ComunicacionAreaService = Depends()):
    try:
        return service.get_all(page, page_size)
    except HTTPException as e:
        raise e

@router.get("/comunicaciones_area/{area_origen_id}/destinos",response_model=List[ComunicacionDestinoResponse],
    description="Obtiene las áreas destino por ID de área de origen"
)
async def get_areas_destino_by_area_origen_id(
    area_origen_id: int,
    service: ComunicacionAreaService = Depends()
):
    try:
        return service.get_areas_destino_by_area_origen_id(area_origen_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))