from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from src.schemas import *
from src.dto.usuario_response_dto import UsuarioResponseDTO
from src.dto.usuario_request_dto import UsuarioRequestDTO
from src.dto.usuario_details_response import UsuarioDetailsResponse
from src.dto.paginated_response import PaginatedResponseDTO
from src.service.imp.usuario_service_imp import UsuarioServiceImp
from src.model.enum.user_status_enum import UserStatusEnum

router = APIRouter(tags=["Usuarios"])
usuarios_metadata = {
    "name": "Usuarios",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Usuario, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Usuario. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post(
    "/usuarios",
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
async def add_usuario(usuario_request: UsuarioRequestDTO, service: UsuarioServiceImp = Depends()):
    return service.add(usuario_request)


@router.get(
    "/usuarios/search",
    response_model=List[UsuarioDetailsResponse],
    description="Busca usuarios por nombre de usuario"
)
async def find_by_string(
    search_string: str = Query(..., description="Nombre del usuario a buscar"),
    service: UsuarioServiceImp = Depends()
):
    return service.find(search_string)


@router.get(
    "/usuarios/paginated",
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
    service: UsuarioServiceImp = Depends()
):
    is_active_bool = is_active == UserStatusEnum.true
    return service.get_paginated(page, page_size, is_active_bool)


@router.put(
    "/usuarios/{usuario_id}",
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
    service: UsuarioServiceImp = Depends()
):
    return service.update(usuario_id, usuario_request)


@router.get(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene un usuario por ID"
)
async def get_usuario(usuario_id: int, service: UsuarioServiceImp = Depends()):
    return service.get_by_id(usuario_id)


@router.patch(
    "/usuarios/{usuario_id}/password",
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
    service: UsuarioServiceImp = Depends()
):
    service.update_password(usuario_id, contrasena)
    return JSONResponse(status_code=200, content={"message": "Contraseña actualizada correctamente"})



@router.delete(
    "/usuarios/{usuario_id}",
    response_model=DeleteSuccessfulResponseSchema,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        404: {"description": "Recurso no encontrado", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Elimina un usuario"
)
async def delete_usuario(usuario_id: int, service: UsuarioServiceImp = Depends()):
    service.delete_by_id(usuario_id)
    return JSONResponse(status_code=200, content={"message": "Usuario eliminado correctamente"})


@router.patch(
    "/usuarios/{usuario_id}/status",
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
    service: UsuarioServiceImp = Depends()
):
    is_active = user_status.value.lower() == "true"
    service.update_status(usuario_id, is_active)
    estado = "activado" if is_active else "desactivado"
    return JSONResponse(status_code=200, content={"message": f"Usuario {estado} correctamente"})


