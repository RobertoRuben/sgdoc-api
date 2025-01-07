from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from src.dto.pagination_response import PaginatedResponse
from src.dto.estado_documento_request import EstadoDocumentoRequest
from src.dto.estado_documento_response import EstadoDocumentoResponse
from src.service.estado_documento_service import EstadoDocumentoService

router = APIRouter(tags=["Estados de Documento"])

estado_documento_tag_metadata={
    "name": "Estados de Documento",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Estado de Documento, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de estados de documentos.",
}

@router.post("/estados-documento", response_model=EstadoDocumentoResponse, description="Crea un nuevo estado de documento")
async def add_estado_documento(estado_documento_request: EstadoDocumentoRequest, service: EstadoDocumentoService = Depends()):
    try:
        return service.add_estado_documento(estado_documento_request)
    except HTTPException as e:
        raise e


@router.get("/estados-documento", response_model=PaginatedResponse, description="Obtiene todos los estados de documento con paginación")
async def get_all_estado_documento(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: EstadoDocumentoService = Depends()
):
    try:
        return service.get_all_estado_documento(page, page_size)
    except HTTPException as e:
        raise e


@router.put("/estados-documento/{estado_documento_id}", response_model=EstadoDocumentoResponse, description="Actualiza un estado de documento")
async def update_estado_documento(estado_documento_id: int, estado_documento_request: EstadoDocumentoRequest, service: EstadoDocumentoService = Depends()):
    try:
        return service.update_estado_documento(estado_documento_id, estado_documento_request)
    except HTTPException as e:
        raise e


@router.delete("/estados-documento/{estado_documento_id}", description="Elimina un estado de documento")
async def delete_estado_documento(estado_documento_id: int, service: EstadoDocumentoService = Depends()):
    try:
        service.delete_documento(estado_documento_id)
        return JSONResponse(content={"message": "Se eliminó el estado de documento correctamente"}, status_code=200)
    except HTTPException as e:
        raise e


@router.get("/estados-documento/documento/{documento_id}", response_model=List[EstadoDocumentoResponse], description="Obtiene todos los estados de documento por ID de documento")
async def get_all_by_documento_id(documento_id: int, service: EstadoDocumentoService = Depends()):
    try:
        return service.get_all_by_id(documento_id)
    except HTTPException as e:
        raise e
