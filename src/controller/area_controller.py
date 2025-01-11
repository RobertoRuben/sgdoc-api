from typing import List
from fastapi import HTTPException, Depends, APIRouter, Query
from fastapi.responses import JSONResponse
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

@router.post("/areas", response_model=AreaResponse, description="Crea un nuevo area")
async def add_area(area_request: AreaRequest, service: AreaService = Depends()):
    try:
        return service.add_area(area_request)
    except HTTPException as e:
        raise e


@router.get("/areas", response_model=List[AreaResponse], description="Obtiene todos los areas")
async def get_areas(service: AreaService = Depends()):
    try:
        return service.get_all_areas()
    except HTTPException as e:
        raise e

@router.get("/areas/search", response_model=List[AreaResponse], description="Busca areas por cadena de búsqueda")
async def search_areas(
    search_string: str = Query(..., description="Cadena de búsqueda para encontrar areas"),
    service: AreaService = Depends()
):
    try:
        return service.find_areas_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/areas/paginated", response_model=PaginatedResponse, description="Obtiene los areas paginados")
async def get_paginated_areas(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: AreaService = Depends()
):
    try:
        return service.get_all_areas_by_pagination(page, page_size)
    except HTTPException as e:
        raise e


@router.get("/areas/{area_id}", response_model=AreaResponse, description="Obtiene un area por su ID")
async def get_area_by_id(area_id: int, service: AreaService = Depends()):
    try:
        return service.get_area_by_id(area_id)
    except HTTPException as e:
        raise e


@router.put("/areas/{area_id}", response_model=AreaResponse, description="Actualiza un area")
async def update_area(area_id: int, area_request: AreaRequest, service: AreaService = Depends()):
    try:
        return service.update_area(area_id, area_request)
    except HTTPException as e:
        raise e


@router.delete("/areas/{area_id}", description="Elimina un area")
async def delete_area_by_id(area_id: int, service: AreaService = Depends()):
    try:
        service.delete_area_by_id(area_id)
        return JSONResponse(content={"message": "Se eliminó el area correctamente"}, status_code=200)
    except HTTPException as e:
        raise e



