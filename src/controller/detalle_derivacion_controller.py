from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.service.detalle_derivacion_service import DetalleDerivacionService
from src.dto.detalle_derivacion_request import DetalleDerivacionRequest
from src.dto.detalle_derivacion_response import DetalleDerivacionResponse

router = APIRouter(tags=["Detalle Derivaciones"])

detalle_derivaciones_tag_metadata={
    "name": "Detalle Derivaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Detalle Derivación, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Detalle Derivación. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post("/detalle_derivaciones", response_model=DetalleDerivacionResponse, description="Crea un nuevo detalle de derivación")
async def add_detalle_derivacion(detalle_derivacion_request: DetalleDerivacionRequest, service: DetalleDerivacionService = Depends()):
    try:
        return service.add_detalle_derivacion(detalle_derivacion_request)
    except HTTPException as e:
        raise e

@router.get("/detalle_derivaciones/{derivacion_id}", response_model=List[DetalleDerivacionResponse], description="Obtiene todos los detalles de derivación de una derivación")
async def get_all_detalle_derivacion_by_id(derivacion_id: int, service: DetalleDerivacionService = Depends()):
    try:
        return service.get_all_detalle_derivacion_by_id(derivacion_id)
    except HTTPException as e:
        raise e

@router.put("/detalle_derivaciones/{detalle_derivacion_id}", response_model=DetalleDerivacionResponse, description="Actualiza un detalle de derivación")
async def update_detalle_derivacion(detalle_derivacion_id: int, detalle_derivacion_request: DetalleDerivacionRequest, service: DetalleDerivacionService = Depends()):
    try:
        return service.update_detalle_derivacion(detalle_derivacion_id, detalle_derivacion_request)
    except HTTPException as e:
        raise

@router.delete("/detalle_derivaciones/{detalle_derivacion_id}", description="Elimina un detalle de derivación")
async def delete_detalle_derivacion(detalle_derivacion_id: int, service: DetalleDerivacionService = Depends()):
    try:
        service.delete_detalle_derivacion_by_id(detalle_derivacion_id)
        return JSONResponse(content={"message": "Se eliminó el detalle de derivación correctamente"}, status_code=200)
    except HTTPException as e:
        raise e