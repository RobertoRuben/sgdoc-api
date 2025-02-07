from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import List
from src.schemas import *
from src.dto import RolRequestDTO, RolReponseDTO, PaginatedResponseDTO
from src.service import RolService
from src.service.imp import RolServiceImp

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

roles_tag_metadata={
    "name": "Roles",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Rol, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Role. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}


def get_rol_service_imp(service: RolServiceImp = Depends()) -> RolService:
    return service


@router.post(
    "/roles",
    response_model=RolReponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo rol"
)
async def add_rol(rol_request: RolRequestDTO, service: RolService = Depends(get_rol_service_imp)):
    return await service.add(rol_request)


@router.get(
    "",
    response_model=List[RolReponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todos los roles"
)
async def get_all_roles(service: RolService = Depends(get_rol_service_imp)):
    return await service.get_all()


@router.get(
    "/search",
    response_model=List[RolReponseDTO],
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Busca roles por cadena de búsqueda"
)
async def search_roles(
    search_string: str = Query(..., min_length=1, description="Cadena de búsqueda para encontrar roles"),
    service: RolService = Depends(get_rol_service_imp)
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
    description="Obtiene los roles paginados"
)
async def get_paginated_roles(
    page: int = Query(1, description="Número de página a obtener"),
    page_size: int = Query(10, description="Número de registros por página"),
    rol_service: RolService = Depends(get_rol_service_imp)
):
    return await rol_service.get_paginated(page, page_size)


@router.get(
    "/{rol_id}",
    response_model=RolReponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un rol por su ID"
)
async def get_rol_by_id(rol_id: int, rol_service: RolService = Depends(get_rol_service_imp)):
    return await rol_service.get_by_id(rol_id)


@router.put(
    "/{rol_id}",
    response_model=RolReponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un rol"
)
async def update_rol(rol_id: int, rol_request: RolRequestDTO, rol_service: RolService = Depends(get_rol_service_imp)):
    return await rol_service.update(rol_id, rol_request)


@router.delete(
    "/{rol_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un rol"
)
async def delete_rol_by_id(rol_id: int, rol_service: RolService = Depends(get_rol_service_imp)):
    await rol_service.delete_by_id(rol_id)
    return JSONResponse(content={"message": "Se eliminó el rol correctamente"}, status_code=200)



