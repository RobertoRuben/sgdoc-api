from typing import List, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.model.entity import Remitente
from src.dto import RemitenteRequestDTO, RemitenteResponseDTO
from src.repository import RemitenteRepository
from src.service import RemitenteService


class RemitenteServiceImp(RemitenteService):
    def __init__(self, remitente_repository: RemitenteRepository = Depends()):
        self.remitente_repository = remitente_repository


    async def add(self, remitente_request: RemitenteRequestDTO) -> RemitenteResponseDTO:
        try:
            exists = await self.remitente_repository.exists(remitente_request.dni)
            if exists:
                raise ConflictException("El DNI ya existe en la base de datos")

            new_remitente = Remitente(
                dni=remitente_request.dni,
                nombres=remitente_request.nombres,
                apellido_paterno=remitente_request.apellido_paterno,
                apellido_materno=remitente_request.apellido_materno,
                genero=remitente_request.genero
            )

            created_remitente = await self.remitente_repository.add_remitentes(new_remitente)

            return RemitenteResponseDTO(
                id=created_remitente.id,
                dni=created_remitente.dni,
                nombres=created_remitente.nombres,
                apellido_paterno=created_remitente.apellido_paterno,
                apellido_materno=created_remitente.apellido_materno,
                genero=created_remitente.genero
            )
        except ConflictException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el remitente",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[RemitenteResponseDTO]:
        try:
            remitentes = await self.remitente_repository.get_all()
            return [
                RemitenteResponseDTO(
                    id=remitente.id,
                    dni=remitente.dni,
                    nombres=remitente.nombres,
                    apellido_paterno=remitente.apellido_paterno,
                    apellido_materno=remitente.apellido_materno,
                    genero=remitente.genero
                ) for remitente in remitentes
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los remitentes",
                error_details=str(e)
            ) from e


    async def update(self, remitente_id: int, remitente_request: RemitenteRequestDTO) -> RemitenteResponseDTO:
        try:
            remitente = await self.remitente_repository.get_by_id(remitente_id)
            if not remitente:
                raise NotFoundException("Remitente no encontrado")

            if remitente.dni == remitente_request.dni:
                return RemitenteResponseDTO(
                    id=remitente.id,
                    dni=remitente.dni,
                    nombres=remitente.nombres,
                    apellido_paterno=remitente.apellido_paterno,
                    apellido_materno=remitente.apellido_materno,
                    genero=remitente.genero
                )

            exists = await self.remitente_repository.exists(remitente_request.dni)
            if exists:
                raise ConflictException("El DNI ya existe en la base de datos")

            remitente.dni = remitente_request.dni
            remitente.nombres = remitente_request.nombres
            remitente.apellido_paterno = remitente_request.apellido_paterno
            remitente.apellido_materno = remitente_request.apellido_materno
            remitente.genero = remitente_request.genero

            updated_remitente = await self.remitente_repository.update_remitente(remitente)

            return RemitenteResponseDTO(
                id=updated_remitente.id,
                dni=updated_remitente.dni,
                nombres=updated_remitente.nombres,
                apellido_paterno=updated_remitente.apellido_paterno,
                apellido_materno=updated_remitente.apellido_materno,
                genero=updated_remitente.genero
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el remitente",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, remitente_id: int) -> None:
        try:
            remitente = await self.remitente_repository.get_by_id(remitente_id)
            if not remitente:
                raise NotFoundException("Remitente no encontrado")
            await self.remitente_repository.delete_by_id(remitente_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el remitente",
                error_details=str(e)
            ) from e


    async def find(self, search_string: str) -> List[RemitenteResponseDTO]:
        try:
            remitentes = await self.remitente_repository.find_by_string(search_string)
            if not remitentes:
                raise NotFoundException("No se encontraron remitentes con la cadena de búsqueda")
            return [
                RemitenteResponseDTO(
                    id=remitente.id,
                    dni=remitente.dni,
                    nombres=remitente.nombres,
                    apellido_paterno=remitente.apellido_paterno,
                    apellido_materno=remitente.apellido_materno,
                    genero=remitente.genero
                ) for remitente in remitentes
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar remitentes",
                error_details=str(e)
            ) from e


    async def get_by_id(self, remitente_id: int) -> RemitenteResponseDTO:
        try:
            remitente = await self.remitente_repository.get_by_id(remitente_id)
            if not remitente:
                raise NotFoundException("Remitente no encontrado")
            return RemitenteResponseDTO(
                id=remitente.id,
                dni=remitente.dni,
                nombres=remitente.nombres,
                apellido_paterno=remitente.apellido_paterno,
                apellido_materno=remitente.apellido_materno,
                genero=remitente.genero
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el remitente",
                error_details=str(e)
            ) from e


    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.remitente_repository.get_all_pagination(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los remitentes paginados",
                error_details=str(e)
            ) from e
