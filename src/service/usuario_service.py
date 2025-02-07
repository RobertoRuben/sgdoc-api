from typing import List, Dict, Any
from fastapi import Depends
from src.exception import NotFoundException, ConflictException
from src.security.argon2_hasher import Argon2PasswordHasher
from src.dto.usuario_details_response import UsuarioDetailsResponse
from src.repository.usuario_repository import UsuarioRepository
from src.model.entity.usuario import Usuario
from src.dto.usuario_request_dto import UsuarioRequestDTO
from src.dto.usuario_response_dto import UsuarioResponseDTO

class UsuarioService:

    def __init__(self, usuario_repository: UsuarioRepository = Depends(), argon_2_security: Argon2PasswordHasher = Depends()):
        self.usuario_repository = usuario_repository
        self.argon_2_security = argon_2_security

    def add_usuario(self, usuario_request: UsuarioRequestDTO) -> UsuarioResponseDTO:

        if self.usuario_repository.exists_by_trabajador_id(usuario_request.trabajador_id):
            raise ConflictException("El trabajador ya tiene un usuario asociado")

        if self.usuario_repository.exists_by_username(usuario_request.nombre_usuario):
            raise ConflictException("El nombre de usuario ya está en uso")

        hashed_contrasena = self.argon_2_security.hash_password(usuario_request.contrasena)

        new_usuario = Usuario(
            nombre_usuario=usuario_request.nombre_usuario,
            contrasena=hashed_contrasena,
            rol_id=usuario_request.rol_id,
            trabajador_id=usuario_request.trabajador_id
        )
        created_usuario = self.usuario_repository.add_usuario(new_usuario)

        return UsuarioResponseDTO(
            id=created_usuario.id,
            nombre_usuario=created_usuario.nombre_usuario,
            fecha_creacion=created_usuario.fecha_creacion,
            fecha_actualizacion=created_usuario.fecha_actualizacion,
            rol_id=created_usuario.rol_id,
            trabajador_id=created_usuario.trabajador_id,
            is_active=created_usuario.is_active
        )


    def get_all_users_by_pagination(self, page: int, page_size: int, is_active: bool) -> Dict[str, Any]:
        users_data = self.usuario_repository.get_usuarios_pagination(page, page_size, is_active)
        return users_data


    def update_user(self, usuario_id, usuario_request: UsuarioRequestDTO) -> UsuarioResponseDTO:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundException("Usuario no encontrado")

        if usuario.nombre_usuario == usuario_request.nombre_usuario and usuario.trabajador_id == usuario_request.trabajador_id:
            return UsuarioResponseDTO(
                id=usuario.id,
                nombre_usuario=usuario.nombre_usuario,
                fecha_creacion=usuario.fecha_creacion,
                fecha_actualizacion=usuario.fecha_actualizacion,
                rol_id=usuario.rol_id,
                trabajador_id=usuario.trabajador_id,
                is_active=usuario.is_active
            )

        if self.usuario_repository.exists_by_trabajador_id(usuario_request.trabajador_id):
            raise ConflictException("El trabajador ya tiene un usuario asociado")

        if self.usuario_repository.exists_by_username(usuario_request.nombre_usuario):
            raise ConflictException("El nombre de usuario ya está en uso")

        hashed_contrasena = self.argon_2_security.hash_password(usuario_request.contrasena)

        usuario.nombre_usuario = usuario_request.nombre_usuario
        usuario.contrasena = hashed_contrasena
        usuario.rol_id = usuario_request.rol_id
        usuario.trabajador_id = usuario_request.trabajador_id

        updated_usuario = self.usuario_repository.update_user(usuario)

        return UsuarioResponseDTO(
            id=updated_usuario.id,
            nombre_usuario=updated_usuario.nombre_usuario,
            fecha_creacion=updated_usuario.fecha_creacion,
            fecha_actualizacion=updated_usuario.fecha_actualizacion,
            rol_id=updated_usuario.rol_id,
            trabajador_id=updated_usuario.trabajador_id,
            is_active=updated_usuario.is_active
        )


    def delete_user(self, usuario_id: int) -> None:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundException("Usuario no encontrado")

        self.usuario_repository.delete_by_id(usuario_id)


    def update_user_status(self, usuario_id: int, active: bool) -> None:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundException("Usuario no encontrado")

        if usuario.is_active == active:
            estado = "activado" if active else "desactivado"
            raise NotFoundException(f"El usuario ya está {estado}")

        self.usuario_repository.update_status_user_by_id(usuario_id, active)


    def find_by_string(self, search_string: str) -> List[UsuarioDetailsResponse]:
        usuarios = self.usuario_repository.find_by_string(search_string)

        if not usuarios:
            raise NotFoundException("No se encontraron usuarios")

        return [
            UsuarioDetailsResponse(
                id=usuario['id'],
                nombre_usuario=usuario['nombre_usuario'],
                fecha_creacion=usuario['fecha_creacion'],
                fecha_actualizacion=usuario['fecha_actualizacion'],
                is_active=usuario['is_active'],
                rol_nombre=usuario['nombre_rol'],
                trabajador_nombre=usuario['nombres']
            ) for usuario in usuarios
        ]


    def get_usuario_by_id(self, usuario_id: int) -> UsuarioResponseDTO:
        usuario = self.usuario_repository.get_by_id(usuario_id)
        if not usuario:
            raise NotFoundException("Usuario no encontrado")

        return UsuarioResponseDTO(
            id=usuario.id,
            nombre_usuario=usuario.nombre_usuario,
            fecha_creacion=usuario.fecha_creacion,
            fecha_actualizacion=usuario.fecha_actualizacion,
            rol_id=usuario.rol_id,
            trabajador_id=usuario.trabajador_id,
            is_active=usuario.is_active
        )


    def update_usuario_password(self, usuario_id: int, contrasena: str) -> None:
        if not contrasena:
            raise NotFoundException("La contraseña no puede estar vacía")
        hashed_contrasena = self.argon_2_security.hash_password(contrasena)

        self.usuario_repository.update_password_by_id(usuario_id, hashed_contrasena)