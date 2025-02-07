from typing import List, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.repository import RolRepository
from src.model.entity import Rol
from src.dto import RolRequestDTO, RolReponseDTO
from src.service import RolService

class RolServiceImp(RolService):
    def __init__(self, rol_repository: RolRepository = Depends()):
        self.rol_repository = rol_repository


    async def add(self, rol_request: RolRequestDTO) -> RolReponseDTO:
        try:
            exists = await self.rol_repository.exists(rol_request.nombre_rol)
            if exists:
                raise ConflictException("El rol ya existe en la base de datos")

            new_rol = Rol(nombre_rol=rol_request.nombre_rol)
            created_rol = await self.rol_repository.add_rol(new_rol)

            return RolReponseDTO(
                id=created_rol.id,
                nombre_rol=created_rol.nombre_rol
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el rol",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[RolReponseDTO]:
        try:
            roles = await self.rol_repository.get_all()
            return [
                RolReponseDTO(
                    id=rol.id,
                    nombre_rol=rol.nombre_rol
                ) for rol in roles
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los roles",
                error_details=str(e)
            ) from e


    async def update(self, rol_id: int, rol_request: RolRequestDTO) -> RolReponseDTO:
        try:
            rol = await self.rol_repository.get_by_id(rol_id)
            if not rol:
                raise NotFoundException("Rol no encontrado")

            if rol.nombre_rol == rol_request.nombre_rol:
                return RolReponseDTO(
                    id=rol.id,
                    nombre_rol=rol.nombre_rol
                )

            exists = await self.rol_repository.exists(rol_request.nombre_rol)
            if exists:
                raise ConflictException("El rol ya existe en la base de datos")

            rol.nombre_rol = rol_request.nombre_rol
            rol = await self.rol_repository.update_rol(rol)

            return RolReponseDTO(
                id=rol.id,
                nombre_rol=rol.nombre_rol
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el rol",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, rol_id: int) -> None:
        try:
            rol = await self.rol_repository.get_by_id(rol_id)
            if not rol:
                raise NotFoundException("Rol no encontrado")
            await self.rol_repository.delete_by_id(rol_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el rol",
                error_details=str(e)
            ) from e


    async def find(self, search_string: str) -> List[RolReponseDTO]:
        try:
            roles = await self.rol_repository.find_by_string(search_string)
            if not roles:
                raise NotFoundException("No se encontraron roles")
            return [
                RolReponseDTO(
                    id=rol.id,
                    nombre_rol=rol.nombre_rol
                ) for rol in roles
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar roles",
                error_details=str(e)
            ) from e


    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.rol_repository.get_all_pagination(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los roles paginados",
                error_details=str(e)
            ) from e


    async def get_by_id(self, rol_id: int) -> RolReponseDTO:
        try:
            rol = await self.rol_repository.get_by_id(rol_id)
            if not rol:
                raise NotFoundException("Rol no encontrado")
            return RolReponseDTO(
                id=rol.id,
                nombre_rol=rol.nombre_rol
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el rol",
                error_details=str(e)
            ) from e
