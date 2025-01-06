from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
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