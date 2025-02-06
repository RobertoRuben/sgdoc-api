from typing import List, Optional, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.model.entity import Caserio
from src.service import CaserioService
from src.dto import CaserioRequestDTO, CaserioResponseDTO
from src.repository import CaserioRepository

class CaserioServiceImp(CaserioService):
    def __init__(self, caserio_repository: CaserioRepository = Depends()):
        self.caserio_repository = caserio_repository


    async def add_caserio(self, caserio_request: CaserioRequestDTO) -> CaserioResponseDTO:
        try:
            exists = await self.caserio_repository.exists(caserio_request.nombre_caserio)
            if exists:
                raise ConflictException("El caserio ya existe")

            caserio = Caserio(
                nombre_caserio=caserio_request.nombre_caserio,
                centro_poblado_id=caserio_request.centro_poblado_id
            )

            created_caserio = await self.caserio_repository.add_caserio(caserio)

            return CaserioResponseDTO(
                id=created_caserio.id,
                nombre_caserio=created_caserio.nombre_caserio,
                centro_poblado_id=created_caserio.centro_poblado_id
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el caserío",
                error_details=str(e)
            ) from e


    async def get_caserios_names(self) -> List[CaserioResponseDTO]:
        try:
            caserios = await self.caserio_repository.get_caserios_names()
            return [
                CaserioResponseDTO(
                    id=caserio.id,
                    nombre_caserio=caserio.nombre_caserio
                ) for caserio in caserios
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los nombres de los caseríos",
                error_details=str(e)
            ) from e


    async def update_caserio(self, caserio_id: int, caserio_request: CaserioRequestDTO) -> CaserioResponseDTO:
        try:
            caserio = await self.caserio_repository.get_caserio_by_id(caserio_id)
            if not caserio:
                raise NotFoundException("El caserio no existe")

            if caserio.nombre_caserio == caserio_request.nombre_caserio:
                return CaserioResponseDTO(
                    id=caserio.id,
                    nombre_caserio=caserio.nombre_caserio,
                    centro_poblado_id=caserio.centro_poblado_id
                )

            exists = await self.caserio_repository.exists(caserio_request.nombre_caserio)
            if exists:
                raise ConflictException("El caserio ya existe")

            caserio.nombre_caserio = caserio_request.nombre_caserio
            caserio.centro_poblado_id = caserio_request.centro_poblado_id

            updated_caserio = await self.caserio_repository.update_caserio(caserio)

            return CaserioResponseDTO(
                id=updated_caserio.id,
                nombre_caserio=updated_caserio.nombre_caserio,
                centro_poblado_id=updated_caserio.centro_poblado_id
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el caserío",
                error_details=str(e)
            ) from e


    async def delete_caserio_by_id(self, caserio_id: int) -> None:
        try:
            caserio = await self.caserio_repository.get_caserio_by_id(caserio_id)
            if not caserio:
                raise NotFoundException("El caserio no existe")

            await self.caserio_repository.delete_caserio_by_id(caserio_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el caserío",
                error_details=str(e)
            ) from e


    async def get_all_caserios_by_centro_poblado_id(self, centro_poblado_id: Optional[int]) -> List[CaserioResponseDTO]:
        try:
            caserios = await self.caserio_repository.get_all_caserios_by_centro_poblado_id(centro_poblado_id)
            return [
                CaserioResponseDTO(
                    id=caserio.id,
                    nombre_caserio=caserio.nombre_caserio,
                    centro_poblado_id=caserio.centro_poblado_id
                ) for caserio in caserios
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los caseríos por centro poblado",
                error_details=str(e)
            ) from e


    async def find_caserio(self, search_string: str) -> List[CaserioResponseDTO]:
        try:
            caserios = await self.caserio_repository.find_by_string(search_string)
            if not caserios:
                raise NotFoundException("No se encontraron caserios")
            return [
                CaserioResponseDTO(
                    id=caserio['id'],
                    nombre_caserio=caserio['nombre_caserio'],
                    centro_poblado_nombre=caserio['nombre_centro_poblado']
                ) for caserio in caserios
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar caseríos",
                error_details=str(e)
            ) from e


    async def get_all_caserios_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.caserio_repository.get_all_paginated(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los caseríos paginados",
                error_details=str(e)
            ) from e


    async def get_caserio_by_id(self, caserio_id: int) -> Optional[CaserioResponseDTO]:
        try:
            caserio = await self.caserio_repository.get_caserio_by_id(caserio_id)
            if not caserio:
                raise NotFoundException("El caserio no existe")
            return CaserioResponseDTO(
                id=caserio.id,
                nombre_caserio=caserio.nombre_caserio,
                centro_poblado_id=caserio.centro_poblado_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el caserío",
                error_details=str(e)
            ) from e
