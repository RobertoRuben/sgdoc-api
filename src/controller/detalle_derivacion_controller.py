from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema
from src.service.detalle_derivacion_service import DetalleDerivacionService
from src.dto.detalle_derivacion_request_dto import DetalleDerivacionRequestDTO
from src.dto.detalle_derivacion_response_dto import DetalleDerivacionResponseDTO
from src.dto.detalle_derivacion_details_response import DetalleDerivacionDetailsResponse

router = APIRouter(tags=["Detalle Derivaciones"])

detalle_derivaciones_tag_metadata={
    "name": "Detalle Derivaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Detalle Derivación, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Detalle Derivación. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post(
    "/detalle-derivaciones",
    response_model=DetalleDerivacionResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo detalle de derivación"
)
async def add_detalle_derivacion(detalle_derivacion_request: DetalleDerivacionRequestDTO, service: DetalleDerivacionService = Depends()):
    return service.add(detalle_derivacion_request)


@router.get(
    "/detalle-derivaciones/{derivacion_id}",
    response_model=List[DetalleDerivacionDetailsResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los detalles de derivación de una derivación"
)
async def get_all_detalle_derivacion_by_id(derivacion_id: int, service: DetalleDerivacionService = Depends()):
    return service.get_paginated_by_id(derivacion_id)


@router.put(
    "/detalle-derivaciones/{detalle_derivacion_id}",
    response_model=DetalleDerivacionDetailsResponse,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un detalle de derivación"
)
async def update_detalle_derivacion(detalle_derivacion_id: int, detalle_derivacion_request: DetalleDerivacionRequestDTO, service: DetalleDerivacionService = Depends()):
    return service.update(detalle_derivacion_id, detalle_derivacion_request)


@router.delete(
    "/detalle-derivaciones/{detalle_derivacion_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un detalle de derivación"
)
async def delete_detalle_derivacion(detalle_derivacion_id: int, service: DetalleDerivacionService = Depends()):
    service.delete_by_id(detalle_derivacion_id)
    return JSONResponse(content={"message": "Se eliminó el detalle de derivación correctamente"}, status_code=200)