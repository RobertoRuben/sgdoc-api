from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import ErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema, ValidationErrorResponseSchema
from src.dto.paginated_response import PaginatedResponseDTO
from src.dto.estado_documento_request import EstadoDocumentoRequest
from src.dto.estado_documento_response import EstadoDocumentoResponse
from src.service.estado_documento_service import EstadoDocumentoService

router = APIRouter(tags=["Estados de Documento"])

estado_documento_tag_metadata={
    "name": "Estados de Documento",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Estado de Documento, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de estados de documentos.",
}

@router.post(
    "/estados-documento",
    response_model=EstadoDocumentoResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo estado de documento"
)
async def add_estado_documento(estado_documento_request: EstadoDocumentoRequest, service: EstadoDocumentoService = Depends()):
    return service.add_estado_documento(estado_documento_request)


@router.get(
    "/estados-documento",
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
    service: EstadoDocumentoService = Depends()
):
    return service.get_all_estado_documento(page, page_size)


@router.put(
    "/estados-documento/{estado_documento_id}",
    response_model=EstadoDocumentoResponse,
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
async def update_estado_documento(estado_documento_id: int, estado_documento_request: EstadoDocumentoRequest, service: EstadoDocumentoService = Depends()):
    return service.update_estado_documento(estado_documento_id, estado_documento_request)


@router.delete(
    "/estados-documento/{estado_documento_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un estado de documento"
)
async def delete_estado_documento(estado_documento_id: int, service: EstadoDocumentoService = Depends()):
    service.delete_documento(estado_documento_id)
    return JSONResponse(content={"message": "Se eliminó el estado de documento correctamente"}, status_code=200)


@router.get(
    "/estados-documento/documento/{documento_id}",
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    response_model=List[EstadoDocumentoResponse],
    description="Obtiene todos los estados de documento por ID de documento"
)
async def get_all_by_documento_id(documento_id: int, service: EstadoDocumentoService = Depends()):
    return service.get_all_by_id(documento_id)
