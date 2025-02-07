from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.model.enum import UserStatusEnum
from src.dto import UsuarioRequestDTO, UsuarioResponseDTO, PaginatedResponseDTO
from src.service import UsuarioService
from src.service.imp import UsuarioServiceImp

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

usuarios_metadata = {
    "name": "Usuarios",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Usuario, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Usuario. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

def get_user_service_imp(service: UsuarioServiceImp = Depends()) -> UsuarioService:
    return service

@router.post(
    "",
    response_model=UsuarioResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea un nuevo usuario"
)
async def add_usuario(usuario_request: UsuarioRequestDTO, service: UsuarioService = Depends(get_user_service_imp)):
    return await service.add(usuario_request)


@router.get(
    "/search",
    response_model=List[UsuarioResponseDTO],
    description="Busca usuarios por nombre de usuario"
)
async def search_usuario(
    search_string: str = Query(..., description="Nombre del usuario a buscar"),
    service: UsuarioService = Depends(get_user_service_imp)
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
    description="Obtiene los usuarios con paginados"
)
async def get_paginated_usuarios(
    page: int = Query(1, description="Número de página a recuperar", ge=1),
    page_size: int = Query(10, description="Número de registros por página", ge=1),
    is_active: UserStatusEnum = Query(
        ...,description="Filtrar usuarios por estado activo (true) o inactivo (false)"
    ),
    service: UsuarioService = Depends(get_user_service_imp)
):
    is_active_bool = is_active == UserStatusEnum.true
    return await service.get_paginated(page, page_size, is_active_bool)


@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza un usuario"
)
async def update_usuario(
    usuario_id: int,
    usuario_request: UsuarioRequestDTO,
    service: UsuarioService = Depends(get_user_service_imp)
):
    return await service.update(usuario_id, usuario_request)


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un usuario por ID"
)
async def get_usuario_by_id(usuario_id: int, service: UsuarioService = Depends(get_user_service_imp)):
    return await service.get_by_id(usuario_id)


@router.patch(
    "/{usuario_id}/update-password",
    response_model=PatchSuccesfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza la contraseña de un usuario"
)
async def update_usuario_password(
    usuario_id: int,
    contrasena: str = Query(..., description="Nueva contraseña del usuario"),
    service: UsuarioService = Depends(get_user_service_imp)
):
    await service.update_password(usuario_id, contrasena)
    return JSONResponse(status_code=200, content={"message": "Contraseña actualizada correctamente"})



@router.delete(
    "/{usuario_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un usuario"
)
async def delete_usuario_by_id(usuario_id: int, service: UsuarioService = Depends(get_user_service_imp)):
    await service.delete_by_id(usuario_id)
    return JSONResponse(status_code=200, content={"message": "Usuario eliminado correctamente"})


@router.patch(
    "/{usuario_id}/update-status",
    response_model=PatchSuccesfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Actualiza el estado de un usuario (activar/desactivar)"
)
async def update_usuario_status(
    usuario_id: int,
    user_status: UserStatusEnum = Query(
        ...,
        description="Estado deseado del usuario: 'true' para activar, 'false' para desactivar"
    ),
    service: UsuarioService = Depends(get_user_service_imp)
):
    is_active = user_status.value.lower() == "true"
    await service.update_status(usuario_id, is_active)
    estado = "activado" if is_active else "desactivado"
    return JSONResponse(status_code=200, content={"message": f"Usuario {estado} correctamente"})


