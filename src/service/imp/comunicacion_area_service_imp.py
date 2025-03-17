from typing import List, Dict, Any
from fastapi import Depends
from src.dto import (
    ComunicacionDestinoResponseDTO,
    ComunicacionAreaRequestDTO,
    ComunicacionAreaSimpleResponseDTO,
    ComunicacionAreaFindResponseDTO
)
from src.exception import NotFoundException, InternalServerException, ConflictException
from src.repository import ComunicacionAreaRepository
from src.model.entity import ComunicacionArea
from src.service import ComunicacionAreaService


class ComunicacionAreaServiceImp(ComunicacionAreaService):
    def __init__(self, comunicacion_area_repository: ComunicacionAreaRepository = Depends()):
        self.comunicacion_area_repository = comunicacion_area_repository


    async def get_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        try:
            return await self.comunicacion_area_repository.get_all_paginated(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las áreas de comunicación paginadas",
                error_details=str(e)
            ) from e


    async def get_paginated_destinos_by_area_origen_id(self, area_origen_id: int) -> List[ComunicacionDestinoResponseDTO]:
        try:
            areas_destinos = await self.comunicacion_area_repository.get_areas_destino_by_area_origen_id(area_origen_id)
            if not areas_destinos:
                raise NotFoundException("No se encontraron áreas destino para el área de origen especificada")
            return [
                ComunicacionDestinoResponseDTO(
                    area_destino_id=area_destino["area_destino_id"],
                    nombre_area_destino=area_destino["nombre_area"]
                ) for area_destino in areas_destinos
            ]
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las áreas destino por área origen",
                error_details=str(e)
            ) from e


    async def add_comunicacion(self, comunicacion_area_request_dto: ComunicacionAreaRequestDTO) -> ComunicacionAreaSimpleResponseDTO:
        try:
            exits = await self.comunicacion_area_repository.exists(comunicacion_area_request_dto.area_origen_id, comunicacion_area_request_dto.area_destino_id)
            if exits:
                raise ConflictException(
                    "La comunicación entre las áreas ya existe",
                )

            new_comunicacion_area = ComunicacionArea(
                area_origen_id=comunicacion_area_request_dto.area_origen_id,
                area_destino_id=comunicacion_area_request_dto.area_destino_id
            )

            created_comunicacion_area = await self.comunicacion_area_repository.add_comunicacion(new_comunicacion_area)
            return ComunicacionAreaSimpleResponseDTO(
                id=created_comunicacion_area.id,
                area_origen_id=created_comunicacion_area.area_origen_id,
                area_destino_id=created_comunicacion_area.area_destino_id
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al agregar la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def get_by_id(self, comunicacion_area_id: int) -> ComunicacionAreaSimpleResponseDTO:
        try:
            comunicacion_area = await self.comunicacion_area_repository.get_by_id(comunicacion_area_id)
            if not comunicacion_area:
                raise NotFoundException("No se encontró la comunicación entre áreas con el ID especificado")
            return ComunicacionAreaSimpleResponseDTO(
                id=comunicacion_area.id,
                area_origen_id=comunicacion_area.area_origen_id,
                area_destino_id=comunicacion_area.area_destino_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener la comunicación entre áreas por ID",
                error_details=str(e)
            ) from e


    async def update_comunicacion(
        self,
        comunicacion_area_id: int,
        comunicacion_area_request_dto: ComunicacionAreaRequestDTO
    ) -> ComunicacionAreaSimpleResponseDTO:
        try:
            comunicacion_area = await self.comunicacion_area_repository.get_by_id(comunicacion_area_id)
            if not comunicacion_area:
                raise NotFoundException("No se encontró la comunicación entre áreas con el ID especificado")

            if comunicacion_area.area_origen_id == comunicacion_area_request_dto.area_origen_id and \
                comunicacion_area.area_destino_id == comunicacion_area_request_dto.area_destino_id:
                return ComunicacionAreaSimpleResponseDTO(
                    id=comunicacion_area.id,
                    area_origen_id=comunicacion_area.area_origen_id,
                    area_destino_id=comunicacion_area.area_destino_id
                )

            exists = await self.comunicacion_area_repository.exists(comunicacion_area_request_dto.area_origen_id, comunicacion_area_request_dto.area_destino_id)
            if exists:
                raise ConflictException("La comunicación entre las áreas ya existe")

            comunicacion_area.area_origen_id = comunicacion_area_request_dto.area_origen_id
            comunicacion_area.area_destino_id = comunicacion_area_request_dto.area_destino_id

            updated_comunicacion_area = await self.comunicacion_area_repository.update_comunicacion(comunicacion_area)
            return ComunicacionAreaSimpleResponseDTO(
                id=updated_comunicacion_area.id,
                area_origen_id=updated_comunicacion_area.area_origen_id,
                area_destino_id=updated_comunicacion_area.area_destino_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def delete_comunicacion(self, comunicacion_area_id: int) -> None:
        try:
            comunicacion_area = await self.comunicacion_area_repository.get_by_id(comunicacion_area_id)
            if not comunicacion_area:
                raise NotFoundException("No se encontró la comunicación entre áreas con el ID especificado")

            await self.comunicacion_area_repository.delete_by_id(comunicacion_area_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar la comunicación entre áreas",
                error_details=str(e)
            ) from e


    async def find(self, search_string: str) -> List[ComunicacionAreaFindResponseDTO]:
        try:
            comunicaciones = await self.comunicacion_area_repository.find_by_area_nombre(search_string)
            return [
                ComunicacionAreaFindResponseDTO(
                    id=comunicacion["id"],
                    nombre_area_origen=comunicacion["area_origen_nombre"],
                    nombre_area_destino=comunicacion["area_destino_nombre"]
                ) for comunicacion in comunicaciones
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar la comunicación entre áreas",
                error_details=str(e)
            ) from e


