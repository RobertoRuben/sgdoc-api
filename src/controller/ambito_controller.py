from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from src.service.ambito_service import AmbitoService
from src.dto.ambito_request import AmbitoRequest
from src.dto.ambito_response import AmbitoResponse
from src.dto.pagination_response import PaginatedResponse

router = APIRouter(tags=["Ambitos"])

ambitos_tag_metadata={
    "name": "Ambitos",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Ambito, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de ambitos documentales.",
}

@router.post("/ambitos", response_model=AmbitoResponse, description="Crea un nuevo ambito documental")
async def add_ambito(ambito_request: AmbitoRequest, service: AmbitoService = Depends()):
    try:
        return service.add_amibito(ambito_request)
    except HTTPException as e:
        raise e


@router.get("/ambitos", response_model=List[AmbitoResponse], description="Obtiene todos los ambitos documentales")
async def get_ambitos(ambito_service: AmbitoService = Depends()):
    try:
        return ambito_service.get_all_ambitos()
    except HTTPException as e:
        raise e

@router.put("/ambitos/{ambito_id}", response_model=AmbitoResponse, description="Actualiza un ambito documental")
async def update_ambito(ambito_id: int, ambito_request: AmbitoRequest, ambito_service: AmbitoService = Depends()):
    try:
        return ambito_service.update_ambito(ambito_id, ambito_request)
    except HTTPException as e:
        raise e


@router.delete("/ambitos/{ambito_id}", description="Elimina un ambito documental")
async def delete_ambito(ambito_id: int, ambito_service: AmbitoService = Depends()):
    try:
        ambito_service.delete_ambito(ambito_id)
        return JSONResponse(content={"message": "Se eliminó el ambito documental correctamente"}, status_code=200)
    except HTTPException as e:
        raise e

@router.get("/ambitos/{ambito_id}", response_model=AmbitoResponse, description="Obtiene un ambito documental por su ID")
async def get_ambito_by_id(ambito_id: int, ambito_service: AmbitoService = Depends()):
    try:
        return ambito_service.get_ambitos_by_id(ambito_id)
    except HTTPException as e:
        raise e


@router.get("/ambitos/search", response_model=List[AmbitoResponse], description="Busca ambitos documentales por cadena de búsqueda")
async def search_ambitos(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar ambitos documentales"),
    ambito_service: AmbitoService = Depends()
):
    try:
        return ambito_service.find_ambito_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/ambitos/paginated", response_model=PaginatedResponse, description="Obtiene los ambitos documentales paginados")
async def get_paginated_ambitos(
    page: int = Query(1, description="Número de página a recuperar"),
    per_page: int = Query(10, description="Número de registros por página"),
    ambito_service: AmbitoService = Depends()
):
    try:
        return ambito_service.get_ambitos_by_pagination(page, per_page)
    except HTTPException as e:
        raise e
