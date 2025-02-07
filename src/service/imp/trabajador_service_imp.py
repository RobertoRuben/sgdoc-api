from typing import List, Dict, Any, Optional
from fastapi import Depends
from src.exception import NotFoundException, ConflictException, InternalServerException
from src.repository import TrabajadorRepository
from src.model.entity import Trabajador
from src.dto import TrabajadorRequestDTO, TrabajadorResponseDTO
from src.service import TrabajadorService

class TrabajadorServiceImp(TrabajadorService):
    def __init__(self, trabajador_repository: TrabajadorRepository = Depends()):
        self.trabajador_repository = trabajador_repository


    async def add(self, trabajador_request: TrabajadorRequestDTO) -> TrabajadorResponseDTO:
        try:
            if await self.trabajador_repository.exists_trabajador_by_dni(trabajador_request.dni):
                raise ConflictException("El trabajador ya existe en la base de datos")

            new_trabajador = Trabajador(
                dni=trabajador_request.dni,
                nombres=trabajador_request.nombres,
                apellido_paterno=trabajador_request.apellido_paterno,
                apellido_materno=trabajador_request.apellido_materno,
                genero=trabajador_request.genero,
                area_id=trabajador_request.area_id,
            )

            created_trabajador = await self.trabajador_repository.add_trabajador(new_trabajador)

            return TrabajadorResponseDTO(
                id=created_trabajador.id,
                dni=created_trabajador.dni,
                nombres=created_trabajador.nombres,
                apellido_paterno=created_trabajador.apellido_paterno,
                apellido_materno=created_trabajador.apellido_materno,
                genero=created_trabajador.genero,
                area_id=created_trabajador.area_id
            )
        except ConflictException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el trabajador",
                error_details=str(e)
            ) from e


    async def get_all_ids_and_names(self) -> List[TrabajadorResponseDTO]:
        try:
            trabajadores = await self.trabajador_repository.get_all_id_and_name()
            return [
                TrabajadorResponseDTO(
                    id=trabajador["id"],
                    nombres=trabajador["nombres"]
                )
                for trabajador in trabajadores
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el listado simple de trabajadores",
                error_details=str(e)
            ) from e


    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            trabajadores_data = await self.trabajador_repository.get_trabajadores_with_area_pagination(page, page_size)
            return trabajadores_data
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener trabajadores paginados",
                error_details=str(e)
            ) from e


    async def update(self, trabajador_id: int, trabajador_request: TrabajadorRequestDTO) -> TrabajadorResponseDTO:
        try:
            trabajador = await self.trabajador_repository.get_by_id(trabajador_id)
            if not trabajador:
                raise NotFoundException("Trabajador no encontrado")

            if trabajador.dni == trabajador_request.dni:
                return TrabajadorResponseDTO(
                    id=trabajador.id,
                    dni=trabajador.dni,
                    nombres=trabajador.nombres,
                    apellido_paterno=trabajador.apellido_paterno,
                    apellido_materno=trabajador.apellido_materno,
                    genero=trabajador.genero,
                    area_id=trabajador.area_id
                )

            if await self.trabajador_repository.exists_trabajador_by_dni(trabajador_request.dni):
                raise ConflictException("El trabajador ya existe en la base de datos")

            trabajador.dni = trabajador_request.dni
            trabajador.nombres = trabajador_request.nombres
            trabajador.apellido_paterno = trabajador_request.apellido_paterno
            trabajador.apellido_materno = trabajador_request.apellido_materno
            trabajador.genero = trabajador_request.genero
            trabajador.area_id = trabajador_request.area_id

            updated_trabajador = await self.trabajador_repository.update_trabajador(trabajador)

            return TrabajadorResponseDTO(
                id=updated_trabajador.id,
                dni=updated_trabajador.dni,
                nombres=updated_trabajador.nombres,
                apellido_paterno=updated_trabajador.apellido_paterno,
                apellido_materno=updated_trabajador.apellido_materno,
                genero=updated_trabajador.genero,
                area_id=updated_trabajador.area_id
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el trabajador",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, trabajador_id: int) -> None:
        try:
            trabajador = await self.trabajador_repository.get_by_id(trabajador_id)
            if not trabajador:
                raise NotFoundException("Trabajador no encontrado")
            await self.trabajador_repository.delete_by_id(trabajador_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el trabajador",
                error_details=str(e)
            ) from e


    async def find(self, search_string: str) -> List[TrabajadorResponseDTO]:
        try:
            trabajadores = await self.trabajador_repository.find_by_string(search_string)
            if not trabajadores:
                raise NotFoundException("No se encontraron trabajadores")
            return [
                TrabajadorResponseDTO(
                    id=trabajador['id'],
                    dni=trabajador['dni'],
                    nombres=trabajador['nombres'],
                    apellido_paterno=trabajador['apellido_paterno'],
                    apellido_materno=trabajador['apellido_materno'],
                    genero=trabajador['genero'],
                    nombre_area=trabajador['nombre_area']
                )
                for trabajador in trabajadores
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar trabajadores",
                error_details=str(e)
            ) from e


    async def get_by_id(self, trabajador_id: int) -> Optional[TrabajadorResponseDTO]:
        try:
            trabajador = await self.trabajador_repository.get_by_id(trabajador_id)
            if not trabajador:
                raise NotFoundException("Trabajador no encontrado")
            return TrabajadorResponseDTO(
                id=trabajador.id,
                dni=trabajador.dni,
                nombres=trabajador.nombres,
                apellido_paterno=trabajador.apellido_paterno,
                apellido_materno=trabajador.apellido_materno,
                genero=trabajador.genero,
                area_id=trabajador.area_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el trabajador",
                error_details=str(e)
            ) from e
