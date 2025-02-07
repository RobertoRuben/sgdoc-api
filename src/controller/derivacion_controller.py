from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema, DeleteSuccessfulResponseSchema
from src.dto.paginated_response import PaginatedResponseDTO
from src.dto.derivacion_request_dto import DerivacionRequestDTO
from src.dto.derivacion_response_dto import DerivacionResponseDTO
from src.service.imp.derivacion_service_imp import DerivacionServiceImp

router = APIRouter(tags=["Derivaciones"])

derivaciones_tag_metadata={
    "name": "Derivaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Derivación, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Derivación. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.get(
    "/derivaciones",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las derivaciones con filtros opcionales y paginación"
)
async def get_derivaciones(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    fecha: Optional[str] = Query(None, description="Filtro por fecha (formato: YYYY-MM-DD)"),
    estado: Optional[str] = Query(None, description="Filtro por estado de la derivación"),
    documento_id: Optional[int] = Query(None, description="Filtro por ID del documento"),
    service: DerivacionServiceImp = Depends()
):
    return service.get_paginated(
        page=page,
        page_size=page_size,
        fecha_filtro=fecha,
        estado_filtro=estado,
        documento_id_filtro=documento_id
    )


@router.post(
    "/derivaciones",
    response_model=DerivacionResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea una nueva derivación"
)
async def add_derivacion(derivacion_request: DerivacionRequestDTO, service: DerivacionServiceImp = Depends()):
    return service.add(derivacion_request)


@router.put(
    "/derivaciones/{derivacion_id}",
    response_model=DerivacionResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza una derivación")
async def update_derivacion(derivacion_id: int, derivacion_request: DerivacionRequestDTO, service: DerivacionServiceImp = Depends()):
    return service.update(derivacion_id, derivacion_request)


@router.delete(
    "/derivaciones/{derivacion_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina una derivación")
async def delete_derivacion(derivacion_id: int, service: DerivacionServiceImp = Depends()):
    service.delete_by_id(derivacion_id)
    return JSONResponse(content={"message": "Se eliminó la derivación correctamente"}, status_code=200)