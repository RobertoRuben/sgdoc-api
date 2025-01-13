from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List
from src.dto.trabajador_response import TrabajadorResponse
from src.dto.trabajador_request import TrabajadorRequest
from src.dto.trabajador_simple_response import TrabajadorSimpleReponse
from src.dto.trabajador_detail_response import TrabajadorDetailResponse
from src.dto.pagination_response import PaginatedResponse
from src.service.trabajador_service import TrabajadorService

router = APIRouter(tags=["Trabajadores"])

trabajadores_tag_metadata={
    "name": "Trabajadores",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Trabajador, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Trabajador. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post("/trabajadores", response_model=TrabajadorResponse, description="Crea un nuevo trabajador")
async def add_trabajador(trabajador_request: TrabajadorRequest, service: TrabajadorService = Depends()):
    try:
        return service.add_trabajador(trabajador_request)
    except HTTPException as e:
        raise e


@router.get("/trabajadores/names", response_model=List[TrabajadorSimpleReponse], description="Obtiene el id y nombres concatenados de los trabajadores")
async def get_all_trabajadores(service: TrabajadorService = Depends()):
    return service.get_all_id_and_trabajador_name()


@router.get("/trabajadores/search", response_model=List[TrabajadorDetailResponse], description="Busca trabajadores por nombre")
async def find_by_string(
    search_string: str = Query(..., description="Nombre del trabajador a buscar"),
    service: TrabajadorService = Depends()
):
    try:
        return service.find_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/trabajadores/paginated", response_model=PaginatedResponse, description="Obtiene los trabajadores con paginados")
async def get_paginated_trabajadores(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: TrabajadorService = Depends()
):
    try:
        return service.get_all_trabajadores_by_pagination(page, page_size)
    except HTTPException as e:
        raise e


@router.get("/trabajadores/{trabajador_id}", response_model=TrabajadorResponse, description="Obtiene un trabajador por id")
async def get_trabajador_by_id(trabajador_id: int, service: TrabajadorService = Depends()):
    try:
        return service.get_trabajador_by_id(trabajador_id)
    except HTTPException as e:
        raise e


@router.put("/trabajadores/{trabajador_id}", response_model=TrabajadorResponse, description="Actualiza un trabajador")
async def update_trabajador(trabajador_id: int, trabajador_request: TrabajadorRequest, service: TrabajadorService = Depends()):
    try:
        return service.update_trabajador(trabajador_id, trabajador_request)
    except HTTPException as e:
        raise e


@router.delete("/trabajadores/{trabajador_id}", description="Elimina un trabajador")
async def delete_trabajador(trabajador_id: int, service: TrabajadorService = Depends()):
    try:
        service.delete_trabajador(trabajador_id)
        return JSONResponse(status_code=200, content={"message": "Trabajador eliminado correctamente"})
    except HTTPException as e:
        raise e




