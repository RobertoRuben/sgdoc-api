from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from src.service.remitente_service import RemitenteService
from src.dto.remitente_request import RemitenteRequest
from src.dto.remitente_response import RemitenteResponse
from src.dto.pagination_response import PaginatedResponse

router = APIRouter(tags=["Remitentes"])

remitentes_tag_metadata={
    "name": "Remitentes",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Remitente, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Remitente. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post("/remitentes", response_model=RemitenteResponse, description="Crea un nuevo remitente")
async def add_remitente(remitente_request: RemitenteRequest, service: RemitenteService = Depends()):
    try:
        return service.add_remitente(remitente_request)
    except HTTPException as e:
        raise e


@router.get("/remitentes", response_model=List[RemitenteResponse], description="Obtiene todos los remitentes")
async def get_remitentes(remitente_service: RemitenteService = Depends()):
    try:
        return remitente_service.get_remitentes()
    except HTTPException as e:
        raise e


@router.put("/remitentes/{remitente_id}", response_model=RemitenteResponse, description="Actualiza un remitente")
async def update_remitente(remitente_id: int, remitente_request: RemitenteRequest, remitente_service: RemitenteService = Depends()):
    try:
        return remitente_service.update_remitente(remitente_id, remitente_request)
    except HTTPException as e:
        raise e


@router.delete("/remitentes/{remitente_id}", description="Elimina un remitente")
async def delete_remitente(remitente_id: int, remitente_service: RemitenteService = Depends()):
    try:
        remitente_service.delete_remitente(remitente_id)
        return JSONResponse(content={"message": "Se eliminó el remitente correctamente"}, status_code=200)
    except HTTPException as e:
        raise e


@router.get("/remitentes/search", response_model=List[RemitenteResponse], description="Busca remitentes por cadena de búsqueda")
async def search_remitentes(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar remitentes"),
    remitente_service: RemitenteService = Depends()
):
    try:
        return remitente_service.find_remitentes_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/remitentes/paginated", response_model=PaginatedResponse, description="Obtiene la lista de remitentes paginada")
async def get_remitentes(page: int = 1, page_size: int = 10, remitente_service: RemitenteService = Depends()):
    try:
        return remitente_service.get_remitentes_with_pagination(page, page_size)
    except HTTPException as e:
        raise e



