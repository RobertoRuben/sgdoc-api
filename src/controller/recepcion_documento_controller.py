from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.dto.recepcion_documento_request import RecepcionDocumentoRequest
from src.dto.recepcion_documento_response import RecepcionDocumentoResponse
from src.service.recepcion_documento_service import RecepcionDocumentoService
from src.dto.pagination_response import PaginatedResponse

router = APIRouter(tags=["Recepcion de Documentos"])

recepcion_documento_tag_metadata={
    "name": "Recepcion de Documentos",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Recepcion de Documentos, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Recepcion de Documentos.",
}

@router.post("/recepcion_documentos", response_model=RecepcionDocumentoResponse, description="Crea una nueva recepcion de documento")
async def add_recepcion_documento(recepcion_documento_request: RecepcionDocumentoRequest, service: RecepcionDocumentoService = Depends()):
    try:
        return service.add_recepcion_documento(recepcion_documento_request)
    except HTTPException as e:
        raise e

@router.get("/recepcion_documentos/paginated", response_model=PaginatedResponse, description="Obtiene todas las recepciones de documentos paginadas")
async def get_all_recepcion_documento_paginated(page: int, size: int, service: RecepcionDocumentoService = Depends()):
    try:
        return service.get_all_recepcion_documento_paginated(page, size)
    except HTTPException as e:
        raise e


@router.put("/recepcion_documentos/{recepcion_id}", response_model=RecepcionDocumentoResponse, description="Actualiza una recepcion de documento")
async def update_recepcion_documento(recepcion_id: int, recepcion_documento_request: RecepcionDocumentoRequest, service: RecepcionDocumentoService = Depends()):
    try:
        return service.update_recepcion_documento(recepcion_id, recepcion_documento_request)
    except HTTPException as e:
        raise e


@router.delete("/recepcion_documentos/{recepcion_id}", description="Elimina una recepcion de documento")
async def delete_recepcion_documento(recepcion_id: int, service: RecepcionDocumentoService = Depends()):
    try:
        service.delete_recepcion_documento(recepcion_id)
        return JSONResponse(content={"message": "Se eliminó la recepcion de documento correctamente"}, status_code=200)
    except HTTPException as e:
        raise e