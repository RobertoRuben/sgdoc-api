from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto import TrabajadorRequestDTO, TrabajadorResponseDTO, PaginatedResponseDTO
from src.service import TrabajadorService
from src.service.imp import TrabajadorServiceImp

router = APIRouter(
    prefix="trabajadores",
    tags=["Trabajadores"]
)

trabajadores_tag_metadata={
    "name": "Trabajadores",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Trabajador, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Trabajador. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}


def get_trabajador_service_imp(service: TrabajadorServiceImp = Depends()) -> TrabajadorService:
    return service


@router.post(
    "",
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
async def add_trabajador(
    trabajador_request: TrabajadorRequestDTO,
    service: TrabajadorService = Depends(get_trabajador_service_imp)):
    return await service.add(trabajador_request)


@router.get(
    "/ids-and-names",
    response_model=List[TrabajadorResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene el id y nombres concatenados de los trabajadores"
)
async def get_ids_and_names(service: TrabajadorService = Depends(get_trabajador_service_imp)):
    return await service.get_all_ids_and_names()


@router.get(
    "/search",
    response_model=List[TrabajadorResponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca trabajadores por nombre"
)
async def search_trabajador(
    search_string: str = Query(..., description="Nombre del trabajador a buscar"),
    service: TrabajadorService = Depends(get_trabajador_service_imp)
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
    description="Obtiene los trabajadores con paginados"
)
async def get_paginated_trabajadores(
    page: int = Query(1, description="Número de página a recuperar"),
    page_size: int = Query(10, description="Número de registros por página"),
    service: TrabajadorService = Depends(get_trabajador_service_imp)
):
    return await service.get_paginated(page, page_size)


@router.get(
    "/{trabajador_id}",
    response_model=TrabajadorResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un trabajador por id"
)
async def get_trabajador_by_id(
    trabajador_id: int,
    service: TrabajadorService = Depends(get_trabajador_service_imp)
):
    return await service.get_by_id(trabajador_id)


@router.put(
    "/{trabajador_id}",
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
async def update_trabajador(
    trabajador_id: int,
    trabajador_request: TrabajadorRequestDTO,
    service: TrabajadorService = Depends(get_trabajador_service_imp)
):
    return await service.update(trabajador_id, trabajador_request)


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
async def delete_trabajador(
    trabajador_id: int,
    service: TrabajadorService = Depends(get_trabajador_service_imp)
):
    await service.delete_by_id(trabajador_id)
    return JSONResponse(
        status_code=200,
        content={"message": "Trabajador eliminado correctamente"}
    )




