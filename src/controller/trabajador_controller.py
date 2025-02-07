from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto.trabajador_response_dto import TrabajadorResponseDTO
from src.dto.trabajador_request_dto import TrabajadorRequestDTO
from src.dto.trabajador_simple_response import TrabajadorSimpleReponse
from src.dto.trabajador_detail_response import TrabajadorDetailResponse
from src.dto.paginated_response import PaginatedResponseDTO
from src.service.imp.trabajador_service_imp import TrabajadorServiceImpl

router = APIRouter(tags=["Trabajadores"])

trabajadores_tag_metadata={
    "name": "Trabajadores",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Trabajador, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Trabajador. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post(
    "/trabajadores",
    response_model=TrabajadorResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo trabajador"
)
async def add_trabajador(trabajador_request: TrabajadorRequestDTO, service: TrabajadorServiceImpl = Depends()):
    return service.add_trabajador(trabajador_request)


@router.get(
    "/trabajadores/names",
    response_model=List[TrabajadorSimpleReponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el id y nombres concatenados de los trabajadores"
)
async def get_all_trabajadores(service: TrabajadorServiceImpl = Depends()):
    return service.get_all_id_and_trabajador_name()


@router.get(
    "/trabajadores/search",
    response_model=List[TrabajadorDetailResponse],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca trabajadores por nombre"
)
async def find_by_string(
    search_string: str = Query(..., description="Nombre del trabajador a buscar"),
    service: TrabajadorServiceImpl = Depends()
):
    return service.find_by_string(search_string)


@router.get(
    "/trabajadores/paginated",
    response_model=PaginatedResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene los trabajadores con paginados"
)
async def get_paginated_trabajadores(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: TrabajadorServiceImpl = Depends()
):
    return service.get_all_trabajadores_by_pagination(page, page_size)


@router.get(
    "/trabajadores/{trabajador_id}",
    response_model=TrabajadorResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un trabajador por id"
)
async def get_trabajador_by_id(trabajador_id: int, service: TrabajadorServiceImpl = Depends()):
    return service.get_trabajador_by_id(trabajador_id)


@router.put(
    "/trabajadores/{trabajador_id}",
    response_model=TrabajadorResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un trabajador"
)
async def update_trabajador(trabajador_id: int, trabajador_request: TrabajadorRequestDTO, service: TrabajadorServiceImpl = Depends()):
    return service.update_trabajador(trabajador_id, trabajador_request)


@router.delete(
    "/trabajadores/{trabajador_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un trabajador"
)
async def delete_trabajador(trabajador_id: int, service: TrabajadorServiceImpl = Depends()):
    service.delete_trabajador(trabajador_id)
    return JSONResponse(status_code=200, content={"message": "Trabajador eliminado correctamente"})




