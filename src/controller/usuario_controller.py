from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import List
from src.dto.usuario_response import UsuarioResponse
from src.dto.usuario_request import UsuarioRequest
from src.dto.usuario_details_response import UsuarioDetailsResponse
from src.dto.pagination_response import PaginatedResponse
from src.service.usuario_service import UsuarioService
from src.model.enum.user_status_enum import UserStatusEnum

router = APIRouter(tags=["Usuarios"])
usuarios_metadata = {
    "name": "Usuarios",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Usuario, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de Usuario. También"
                   " ofrece funcionalidades de paginación y conteo de registros.",
}

@router.post("/usuarios", response_model=UsuarioResponse, description="Crea un nuevo usuario")
async def add_usuario(usuario_request: UsuarioRequest, service: UsuarioService = Depends()):
    try:
        return service.add_usuario(usuario_request)
    except HTTPException as e:
        raise e


@router.get("/usuarios/search", response_model=List[UsuarioDetailsResponse], description="Busca usuarios por nombre de usuario")
async def find_by_string(
    search_string: str = Query(..., description="Nombre del usuario a buscar"),
    service: UsuarioService = Depends()
):
    try:
        return service.find_by_string(search_string)
    except HTTPException as e:
        raise e


@router.get("/usuarios/paginated", response_model=PaginatedResponse, description="Obtiene los usuarios con paginados")
async def get_paginated_usuarios(
    page: int = Query(1, description="Número de página a recuperar", ge=1),
    page_size: int = Query(10, description="Número de registros por página", ge=1),
    is_active: UserStatusEnum = Query(
        ...,
        description="Filtrar usuarios por estado activo (true) o inactivo (false)"
    ),
    service: UsuarioService = Depends()
):
    is_active_bool = is_active == UserStatusEnum.true
    try:
        return service.get_all_users_by_pagination(page, page_size, is_active_bool)
    except HTTPException as e:
        raise e


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse, description="Actualiza un usuario")
async def update_usuario(
    usuario_id: int,
    usuario_request: UsuarioRequest,
    service: UsuarioService = Depends()
):
    try:
        return service.update_user(usuario_id, usuario_request)
    except HTTPException as e:
        raise e


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, description="Obtiene un usuario por ID")
async def get_usuario(usuario_id: int, service: UsuarioService = Depends()):
    try:
        return service.get_usuario_by_id(usuario_id)
    except HTTPException as e:
        raise e


@router.patch("/usuarios/{usuario_id}/password", description="Actualiza la contraseña de un usuario")
async def update_usuario_password(
    usuario_id: int,
    contrasena: str = Query(..., description="Nueva contraseña del usuario"),
    service: UsuarioService = Depends()
):
    try:
        service.update_usuario_password(usuario_id, contrasena)
        return JSONResponse(status_code=200, content={"message": "Contraseña actualizada correctamente"})
    except HTTPException as e:
        raise e


@router.delete("/usuarios/{usuario_id}", description="Elimina un usuario")
async def delete_usuario(usuario_id: int, service: UsuarioService = Depends()):
    try:
        service.delete_user(usuario_id)
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado correctamente"})
    except HTTPException as e:
        raise e


@router.patch(
    "/usuarios/{usuario_id}/status",
    description="Actualiza el estado de un usuario (activar/desactivar)"
)
async def update_usuario_status(
    usuario_id: int,
    user_status: UserStatusEnum = Query(
        ...,
        description="Estado deseado del usuario: 'true' para activar, 'false' para desactivar"
    ),
    service: UsuarioService = Depends()
):
    try:
        is_active = user_status.value.lower() == "true"

        service.update_user_status(usuario_id, is_active)

        estado = "activado" if is_active else "desactivado"
        return JSONResponse(status_code=200, content={"message": f"Usuario {estado} correctamente"})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


