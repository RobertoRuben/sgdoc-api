from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from src.service.caserio_service import CaserioService
from src.dto.caserio_request import CaserioRequest
from src.dto.caserio_response import CaserioResponse, CaserioResponseWithCentroPobladoId
from src.dto.pagination_response import PaginatedResponse


router = APIRouter(tags=["Caserios"])

caserios_tag_metadata={
    "name": "Caserios",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Caserio, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de caserios.",
}

@router.post("/caserios", response_model=CaserioResponseWithCentroPobladoId, description="Crea un nuevo caserio")
async def add_caserio(caserio_request: CaserioRequest, service: CaserioService = Depends()):
    try:
        return service.add_caserio(caserio_request)
    except HTTPException as e:
        raise e


@router.get("/caserios", response_model=List[CaserioResponseWithCentroPobladoId], description="Obtiene todos los caserios")
async def get_caserios_by_centro_poblado_id(centro_poblado_id: int | None = Query(None), caserio_service: CaserioService = Depends()):
    try:
        return caserio_service.get_all_caserios_by_centro_poblado_id(centro_poblado_id)
    except HTTPException as e:
        raise e


@router.get("/caserios/paginated", response_model=PaginatedResponse, description="Obtiene los caserios con paginados")
async def get_paginated_caserios(
    page: int = Query(1, description="Número de página a recuperar"),
    per_page: int = Query(10, description="Número de registros por página"),
    caserio_service: CaserioService = Depends()
):
    try:
        return caserio_service.get_all_caserios_by_pagination(page, per_page)
    except HTTPException as e:
        raise e