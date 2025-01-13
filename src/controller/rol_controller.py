from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List
from src.dto.rol_request import RolRequest
from src.dto.rol_response import RolReponse
from src.dto.pagination_response import PaginatedResponse
from src.service.rol_service import RolService

router = APIRouter(tags=["Roles"])

roles_tag_metadata={
    "name": "Roles",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Rol, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Role. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post("/roles", response_model=RolReponse, description="Crea un nuevo rol")
async def add_rol(rol_request: RolRequest, service: RolService = Depends()):
    try:
        return service.add_rol(rol_request)
    except HTTPException as e:
        raise e


@router.get("/roles", response_model=List[RolReponse], description="Obtiene todos los roles")
async def get_roles(rol_service: RolService = Depends()):
    try:
        return rol_service.get_roles()
    except HTTPException as e:
        raise e


@router.get("/roles/search", response_model=List[RolReponse], description="Busca roles por cadena de búsqueda")
async def search_roles(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar roles"),
    rol_service: RolService = Depends()
):
    try:
        return rol_service.find_rol_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/roles/paginated", response_model=PaginatedResponse, description="Obtiene los roles paginados")
async def get_paginated_roles(
    page: int = Query(1, description="Número de página a obtener"),
    page_size: int = Query(10, description="Número de registros por página"),
    rol_service: RolService = Depends()
):
    try:
        return rol_service.get_roles_with_pagination(page, page_size)
    except HTTPException as e:
        raise e


@router.get("/roles/{rol_id}", response_model=RolReponse, description="Obtiene un rol por su ID")
async def get_rol_by_id(rol_id: int, rol_service: RolService = Depends()):
    try:
        return rol_service.get_rol_id(rol_id)
    except HTTPException as e:
        raise e


@router.put("/roles/{rol_id}", response_model=RolReponse, description="Actualiza un rol")
async def update_rol(rol_id: int, rol_request: RolRequest, rol_service: RolService = Depends()):
    try:
        return rol_service.update_rol(rol_id, rol_request)
    except HTTPException as e:
        raise e


@router.delete("/roles/{rol_id}", description="Elimina un rol")
async def delete_rol(rol_id: int, rol_service: RolService = Depends()):
    try:
        rol_service.delete_rol(rol_id)
        return JSONResponse(content={"message": "Se eliminó el rol correctamente"}, status_code=200)
    except HTTPException as e:
        raise e



