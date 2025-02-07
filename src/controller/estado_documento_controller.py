from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto import EstadoDocumentoRequestDTO, EstadoDocumentoResponseDTO, PaginatedResponseDTO
from src.service import EstadoDocumentoService
from src.service.imp import EstadoDocumentoServiceImp

router = APIRouter(
    prefix="/estados-documento",
    tags=["Estados de Documento"]
)

estado_documento_tag_metadata={
    "name": "Estados de Documento",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Estado de Documento, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de estados de documentos.",
}


def get_estado_documento_service_imp(service: EstadoDocumentoServiceImp = Depends()) -> EstadoDocumentoService:
    return service

@router.post(
    "",
    response_model=EstadoDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo estado de documento"
)
async def add_estado_documento(
    estado_documento_request: EstadoDocumentoRequestDTO,
    service: EstadoDocumentoService = Depends(get_estado_documento_service_imp)
):
    return await service.add(estado_documento_request)


@router.get(
    "",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los estados de documento con paginación"
)
async def get_all_estado_documento(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: EstadoDocumentoService = Depends(get_estado_documento_service_imp)
):
    return await service.get_all(page, page_size)



@router.put(
    "/{estado_documento_id}",
    response_model=EstadoDocumentoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un estado de documento"
)
async def update_estado_documento(
    estado_documento_id: int,
    estado_documento_request: EstadoDocumentoRequestDTO,
    service: EstadoDocumentoService = Depends(get_estado_documento_service_imp)
):
    return await service.update(estado_documento_id, estado_documento_request)


@router.delete(
    "/{estado_documento_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un estado de documento"
)
async def delete_estado_documento(
    estado_documento_id: int,
    service: EstadoDocumentoService = Depends(get_estado_documento_service_imp)
):
    await service.delete_by_id(estado_documento_id)
    return JSONResponse(
        content={"message": "Se eliminó el estado de documento correctamente"},
        status_code=200
    )


@router.get(
    "/estados-documento/documento/{documento_id}",
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    response_model=List[EstadoDocumentoResponseDTO],
    description="Obtiene todos los estados de documento por ID de documento"
)
async def get_all_by_documento_id(documento_id: int, service: EstadoDocumentoServiceImp = Depends()):
    return service.get_all_by_documento_id(documento_id)
