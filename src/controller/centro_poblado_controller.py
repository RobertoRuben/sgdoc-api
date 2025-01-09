from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from src.dto.centro_poblado_response import CentroPobladoResponse
from src.dto.centro_poblado_request import CentroPobladoRequest
from src.dto.pagination_response import PaginatedResponse
from src.service.centro_poblado_service import CentroPobladoService

router = APIRouter(tags=["Centros Poblados"])

centros_poblados_tag_metadata={
    "name": "Centros Poblados",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Centro Poblado, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Centro Poblado.",
}


@router.post("/centros-poblados", response_model=CentroPobladoResponse, description="Crea un nuevo centro poblado")
async def add_centro_poblado(centro_poblado_request: CentroPobladoRequest, service: CentroPobladoService = Depends()):
    try:
        return service.add_centro_poblado(centro_poblado_request)
    except HTTPException as e:
        raise e


@router.get("/centros-poblados", response_model=List[CentroPobladoResponse], description="Obtiene todos los centros poblados")
async def get_centros_poblados(centro_poblado_service: CentroPobladoService = Depends()):
    try:
        return centro_poblado_service.get_all_centros_poblados()
    except HTTPException as e:
        raise e

@router.get("/centros-poblados/search", response_model=List[CentroPobladoResponse], description="Busca centros poblados por cadena de búsqueda")
async def search_centros_poblados(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar centros poblados"),
    centro_poblado_service: CentroPobladoService = Depends()
):
    try:
        return centro_poblado_service.find_centro_poblado_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/centros-poblados/paginated", response_model=PaginatedResponse, description="Obtiene los centros poblados paginados")
async def get_paginated_centros_poblados(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    centro_poblado_service: CentroPobladoService = Depends()
):
    try:
        return centro_poblado_service.get_all_centros_poblados_paginated(page, page_size)
    except HTTPException as e:
        raise e



@router.put("/centros-poblados/{centro_poblado_id}", response_model=CentroPobladoResponse, description="Actualiza un centro poblado")
async def update_centro_poblado(centro_poblado_id: int, centro_poblado_request: CentroPobladoRequest, centro_poblado_service: CentroPobladoService = Depends()):
    try:
        return centro_poblado_service.update_centro_poblado(centro_poblado_id, centro_poblado_request)
    except HTTPException as e:
        raise e


@router.delete("/centros-poblados/{centro_poblado_id}", description="Elimina un centro poblado")
async def delete_centro_poblado(centro_poblado_id: int, centro_poblado_service: CentroPobladoService = Depends()):
    try:
        centro_poblado_service.delete_centro_poblado_by_id(centro_poblado_id)
        return JSONResponse(content={"message": "Se eliminó el centro poblado correctamente"}, status_code=200)
    except HTTPException as e:
        raise e


@router.get("/centros-poblados/{centro_poblado_id}", response_model=CentroPobladoResponse, description="Obtiene un centro poblado por su ID")
async def get_centro_poblado_by_id(centro_poblado_id: int, centro_poblado_service: CentroPobladoService = Depends()):
    try:
        return centro_poblado_service.get_centro_poblado_by_id(centro_poblado_id)
    except HTTPException as e:
        raise e