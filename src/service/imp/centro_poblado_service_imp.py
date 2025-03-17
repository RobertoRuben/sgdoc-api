from typing import List, Dict, Any
from fastapi import Depends
from src.exception import NotFoundException, ConflictException, InternalServerException
from src.model.entity import CentroPoblado
from src.dto import CentroPobladoRequestDTO, CentroPobladoResponseDTO
from src.repository import CentroPobladoRepository
from src.service import CentroPobladoService

class CentroPobladoServiceImp(CentroPobladoService):
    def __init__(self, centro_poblado_repository: CentroPobladoRepository = Depends()):
        self.centro_poblado_repository = centro_poblado_repository


    async def add(self, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        try:
            exists = await self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado)
            if exists:
                raise ConflictException("El centro poblado ya existe en la base de datos")

            new_centro_poblado = CentroPoblado(
                nombre_centro_poblado=centro_poblado_request.nombre_centro_poblado
            )

            created_centro_poblado = await self.centro_poblado_repository.add_centro_poblado(new_centro_poblado)

            return CentroPobladoResponseDTO(
                id=created_centro_poblado.id,
                nombre_centro_poblado=created_centro_poblado.nombre_centro_poblado
            )
        except ConflictException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el centro poblado",
                error_details=str(e)
            ) from e


    async def get_all(self) -> List[CentroPobladoResponseDTO]:
        try:
            centros_poblados = await self.centro_poblado_repository.get_all()
            return [
                CentroPobladoResponseDTO(
                    id=centro_poblado.id,
                    nombre_centro_poblado=centro_poblado.nombre_centro_poblado
                ) for centro_poblado in centros_poblados
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los centros poblados",
                error_details=str(e)
            ) from e


    async def update(self, centro_poblado_id: int, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        try:
            centro_poblado = await self.centro_poblado_repository.get_by_id(centro_poblado_id)
            if not centro_poblado:
                raise NotFoundException("Centro poblado no encontrado")

            if centro_poblado.nombre_centro_poblado == centro_poblado_request.nombre_centro_poblado:
                return CentroPobladoResponseDTO(
                    id=centro_poblado.id,
                    nombre_centro_poblado=centro_poblado.nombre_centro_poblado
                )

            exists = await self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado)
            if exists:
                raise ConflictException("El centro poblado ya existe en la base de datos")

            centro_poblado.nombre_centro_poblado = centro_poblado_request.nombre_centro_poblado

            updated_centro_poblado = await self.centro_poblado_repository.update_centro_poblado(centro_poblado)

            return CentroPobladoResponseDTO(
                id=updated_centro_poblado.id,
                nombre_centro_poblado=updated_centro_poblado.nombre_centro_poblado
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el centro poblado",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, centro_poblado_id: int) -> None:
        try:
            centro_poblado = await self.centro_poblado_repository.get_by_id(centro_poblado_id)
            if not centro_poblado:
                raise NotFoundException("Centro poblado no encontrado")

            await self.centro_poblado_repository.delete_by_id(centro_poblado_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el centro poblado",
                error_details=str(e)
            ) from e


    async def find(self, search_string: str) -> List[CentroPobladoResponseDTO]:
        try:
            centros_poblados = await self.centro_poblado_repository.find_by_string(search_string)
            if not centros_poblados:
                raise NotFoundException("Centro poblado no encontrado")

            return [
                CentroPobladoResponseDTO(
                    id=centro_poblado.id,
                    nombre_centro_poblado=centro_poblado.nombre_centro_poblado
                ) for centro_poblado in centros_poblados
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar el centro poblado",
                error_details=str(e)
            ) from e


    async def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.centro_poblado_repository.get_all_paginated(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los centros poblados paginados",
                error_details=str(e)
            ) from e


    async def get_by_id(self, centro_poblado_id: int) -> CentroPobladoResponseDTO:
        try:
            centro_poblado = await self.centro_poblado_repository.get_by_id(centro_poblado_id)
            if not centro_poblado:
                raise NotFoundException("Centro poblado no encontrado")

            return CentroPobladoResponseDTO(
                id=centro_poblado.id,
                nombre_centro_poblado=centro_poblado.nombre_centro_poblado
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el centro poblado",
                error_details=str(e)
            ) from e
