from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto import CentroPobladoRequestDTO, CentroPobladoResponseDTO, PaginatedResponseDTO
from src.service import CentroPobladoService
from src.service.imp import CentroPobladoServiceImp


def get_centro_poblado_imp(service: CentroPobladoServiceImp = Depends()) -> CentroPobladoService:
    return service


router = APIRouter(
    prefix="/centros-poblados",
    tags=["Centros Poblados"]
)

centros_poblados_tag_metadata={
    "name": "Centros Poblados",
    "description": "Esta sección proporciona los endpoints para gestionar las entidades de Centro Poblado, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de Centro Poblado.",
}


@router.post(
    "",
    response_model=CentroPobladoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo centro poblado"
)
async def add_centro_poblado(
    centro_poblado_request: CentroPobladoRequestDTO,
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    return await service.add(centro_poblado_request)


@router.get(
    "",
    response_model=List[CentroPobladoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los centros poblados"
)
async def get_all_centros_poblados(service: CentroPobladoService = Depends(get_centro_poblado_imp)):
    return await service.get_all()


@router.get(
    "/search",
    response_model=List[CentroPobladoResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca centros poblados por cadena de búsqueda"
)
async def search_centros_poblados(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar centros poblados"),
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    return await service.find(search_string)


@router.get(
    "/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los centros poblados paginados"
)
async def get_paginated_centros_poblados(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    return await service.get_paginated(page, page_size)



@router.get(
    "/{centro_poblado_id}",
    response_model=CentroPobladoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un centro poblado por su ID")
async def get_centro_poblado_by_id(
    centro_poblado_id: int,
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    return await service.get_by_id(centro_poblado_id)


@router.put(
    "/centros-poblados/{centro_poblado_id}",
    response_model=CentroPobladoResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un centro poblado"
)
async def update_centro_poblado(
    centro_poblado_id: int,
    centro_poblado_request: CentroPobladoRequestDTO,
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    return await service.update(centro_poblado_id, centro_poblado_request)


@router.delete(
    "/{centro_poblado_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un centro poblado"
)
async def delete_centro_poblado_by_id(
    centro_poblado_id: int,
    service: CentroPobladoService = Depends(get_centro_poblado_imp)
):
    await service.delete_by_id(centro_poblado_id)
    return JSONResponse(
        content={"message": "Se eliminó el centro poblado correctamente"},
        status_code=200
    )
