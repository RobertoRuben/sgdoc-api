from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from src.service.categoria_service import CategoriaService
from src.dto.categoria_request import CategoriaRequest
from src.dto.categoria_response import CategoriaResponse
from src.dto.pagination_response import PaginatedResponse

router = APIRouter(tags=["Categorias"])

categorias_tag_metadata={
    "name": "Categorias",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Categoria, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Categoria.",
}

@router.post("/categorias", response_model=CategoriaResponse, description="Crea una nueva categoria")
async def add_categoria(categoria_request: CategoriaRequest, service: CategoriaService = Depends()):
    try:
        return service.add_categoria(categoria_request)
    except HTTPException as e:
        raise e

@router.get("/categorias", response_model=List[CategoriaResponse], description="Obtiene todas las categorias")
async def get_categorias(categoria_service: CategoriaService = Depends()):
    try:
        return categoria_service.get_categorias()
    except HTTPException as e:
        raise e

@router.get("/categorias/search", response_model=List[CategoriaResponse], description="Busca categorias por cadena de búsqueda")
async def search_categorias(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar categorias"),
    categoria_service: CategoriaService = Depends()
):
    try:
        return categoria_service.find_categoria_by_string(search_string)
    except HTTPException as e:
        raise e

@router.get("/categorias/paginated", response_model=PaginatedResponse, description="Obtiene las categorias paginadas")
async def get_paginated_categorias(
    page: int = Query(1, description="Número de página a recuperar"),
    per_page: int = Query(10, description="Número de registros por página"),
    categoria_service: CategoriaService = Depends()
):
    try:
        return categoria_service.get_categorias_by_pagination(page, per_page)
    except HTTPException as e:
        raise e

@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse, description="Actualiza una categoria")
async def update_categoria(categoria_id: int, categoria_request: CategoriaRequest, categoria_service: CategoriaService = Depends()):
    try:
        return categoria_service.update_categoria(categoria_id, categoria_request)
    except HTTPException as e:
        raise e

@router.delete("/categorias/{categoria_id}", description="Elimina una categoria")
async def delete_categoria(categoria_id: int, categoria_service: CategoriaService = Depends()):
    try:
        categoria_service.delete_categoria(categoria_id)
        return JSONResponse(content={"message": "Se eliminó la categoria correctamente"}, status_code=200)
    except HTTPException as e:
        raise e

@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse, description="Obtiene una categoria por su ID")
async def get_categoria_by_id(categoria_id: int, categoria_service: CategoriaService = Depends()):
    try:
        return categoria_service.get_categoria_by_id(categoria_id)
    except HTTPException as e:
        raise e



