from typing import List, Any, Dict
from fastapi import Depends
from src.service import AreaService
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.dto import AreaRequestDTO, AreaResponseDTO
from src.model.entity import Area
from src.repository.area_repository import AreaRepository

class AreaServiceImpl(AreaService):
    def __init__(self, area_repository: AreaRepository = Depends()):
        self.area_repository = area_repository

    async def add_area(self, area_request: AreaRequestDTO) -> AreaResponseDTO:
        try:
            exists = await self.area_repository.exists(area_request.nombre_area)
            if exists:
                raise ConflictException("El area ya existe")

            area = Area(nombre_area=area_request.nombre_area)
            created_area = await self.area_repository.add_area(area)

            return AreaResponseDTO(
                id=created_area.id,
                nombre_area=created_area.nombre_area
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el área",
                error_details=str(e)
            ) from e


    async def get_all_areas(self) -> List[AreaResponseDTO]:
        try:
            areas = await self.area_repository.get_all_areas()
            return [
                AreaResponseDTO(
                    id=area.id,
                    nombre_area=area.nombre_area
                ) for area in areas
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las areas",
                error_details=str(e)
            ) from e


    async def update_area(self, area_id: int, area_request: AreaRequestDTO) -> AreaResponseDTO:
        try:
            area = await self.area_repository.get_area_by_id(area_id)
            if not area:
                raise NotFoundException("El area no existe")

            if area.nombre_area == area_request.nombre_area:
                return AreaResponseDTO(
                    id=area.id,
                    nombre_area=area.nombre_area
                )

            exists = await self.area_repository.exists(area_request.nombre_area)
            if exists:
                raise ConflictException("El area ya existe")

            area.nombre_area = area_request.nombre_area
            updated_area = await self.area_repository.update_area(area)

            return AreaResponseDTO(
                id=updated_area.id,
                nombre_area=updated_area.nombre_area
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el area",
                error_details=str(e)
            ) from e


    async def delete_area_by_id(self, area_id: int) -> None:
        try:
            area = await self.area_repository.get_area_by_id(area_id)
            if not area:
                raise NotFoundException("El area no existe")

            await self.area_repository.delete_area_by_id(area_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el area",
                error_details=str(e)
            ) from e


    async def find_area(self, search_string: str) -> List[AreaResponseDTO]:
        try:
            areas = await self.area_repository.find_by_string(search_string)
            if not areas:
                raise NotFoundException("No se encontraron areas")
            return [
                AreaResponseDTO(
                    id=area.id,
                    nombre_area=area.nombre_area
                ) for area in areas
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar areas",
                error_details=str(e)
            ) from e


    async def get_all_areas_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.area_repository.get_all_pagination(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener areas paginadas",
                error_details=str(e)
            ) from e


    async def get_area_by_id(self, area_id: int) -> AreaResponseDTO:
        try:
            area = await self.area_repository.get_area_by_id(area_id)
            if not area:
                raise NotFoundException("El area no existe")
            return AreaResponseDTO(
                id=area.id,
                nombre_area=area.nombre_area
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el area",
                error_details=str(e)
            ) from e
