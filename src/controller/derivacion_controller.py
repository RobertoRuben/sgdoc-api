from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List
from src.dto.pagination_response import PaginatedResponse
from src.dto.derivacion_request import DerivacionRequest
from src.dto.derivacion_response import DerivacionResponse
from src.service.derivacion_service import DerivacionService

router = APIRouter(tags=["Derivaciones"])

derivaciones_tag_metadata={
    "name": "Derivaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Derivación, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Derivación. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.get(
    "/derivaciones",
    response_model=PaginatedResponse,
    description="Obtiene todas las derivaciones con filtros opcionales y paginación"
)
async def get_derivaciones(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    fecha: Optional[str] = Query(None, description="Filtro por fecha (formato: YYYY-MM-DD)"),
    estado: Optional[str] = Query(None, description="Filtro por estado de la derivación"),
    documento_id: Optional[int] = Query(None, description="Filtro por ID del documento"),
    service: DerivacionService = Depends()
):
    try:
        return service.get_all_derivaciones(
            page=page,
            page_size=page_size,
            fecha_filtro=fecha,
            estado_filtro=estado,
            documento_id_filtro=documento_id
        )
    except HTTPException as e:
        raise e

@router.post("/derivaciones", response_model=DerivacionResponse, description="Crea una nueva derivación")
async def add_derivacion(derivacion_request: DerivacionRequest, service: DerivacionService = Depends()):
    try:
        return service.add_derivacion(derivacion_request)
    except HTTPException as e:
        raise e


@router.put("/derivaciones/{derivacion_id}", response_model=DerivacionResponse, description="Actualiza una derivación")
async def update_derivacion(derivacion_id: int, derivacion_request: DerivacionRequest, service: DerivacionService = Depends()):
    try:
        return service.update_derivacion(derivacion_id, derivacion_request)
    except HTTPException as e:
        raise e


@router.delete("/derivaciones/{derivacion_id}", description="Elimina una derivación")
async def delete_derivacion(derivacion_id: int, service: DerivacionService = Depends()):
    try:
        service.delete_derivacion(derivacion_id)
        return JSONResponse(content={"message": "Se eliminó la derivación correctamente"}, status_code=200)
    except HTTPException as e:
        raise e