from typing import List, Optional, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException
from src.model.entity.caserio import Caserio
from src.dto.caserio_request_dto import CaserioRequestDTO
from src.dto.caserio_response_dto import CaserioResponseDTO, CaserioResponseWithCentroPobladoId, CaserioSimpleResponse
from src.repository.caserio_repository import CaserioRepository

class CaserioService:

    def __init__(self, caserio_repository: CaserioRepository = Depends()):
        self.caserio_repository = caserio_repository


    def add_caserio(self, caserio_request: CaserioRequestDTO) -> CaserioResponseWithCentroPobladoId:
        if self.caserio_repository.exists(caserio_request.nombre_caserio):
            raise ConflictException("El caserio ya existe")

        caserio = Caserio(
            nombre_caserio=caserio_request.nombre_caserio,
            centro_poblado_id=caserio_request.centro_poblado_id
        )

        caserio = self.caserio_repository.add_caserio(caserio)

        return CaserioResponseWithCentroPobladoId(
            id=caserio.id,
            nombre_caserio=caserio.nombre_caserio,
            centro_poblado_id=caserio.centro_poblado_id
        )


    def get_caserios_names(self) -> List[CaserioSimpleResponse]:
        caserios = self.caserio_repository.get_caserios_names()

        return [
            CaserioSimpleResponse(
                id=caserio.id,
                nombre_caserio=caserio.nombre_caserio
            ) for caserio in caserios
        ]


    def update_caserio(self, caserio_id: int, caserio_request: CaserioRequestDTO) -> CaserioResponseWithCentroPobladoId:
        caserio = self.caserio_repository.get_caserio_by_id(caserio_id)
        if not caserio:
            raise NotFoundException("El caserio no existe")

        if caserio.nombre_caserio == caserio_request.nombre_caserio:
            return CaserioResponseWithCentroPobladoId(
                id=caserio.id,
                nombre_caserio=caserio.nombre_caserio,
                centro_poblado_id=caserio.centro_poblado_id
            )

        if self.caserio_repository.exists(caserio_request.nombre_caserio):
            raise ConflictException("El caserio ya existe")

        caserio.nombre_caserio = caserio_request.nombre_caserio
        caserio.centro_poblado_id = caserio_request.centro_poblado_id

        caserio = self.caserio_repository.update_caserio(caserio)

        return CaserioResponseWithCentroPobladoId(
            id=caserio.id,
            nombre_caserio=caserio.nombre_caserio,
            centro_poblado_id=caserio.centro_poblado_id
        )


    def delete_caserio_by_id(self, caserio_id: int) -> None:
        caserio = self.caserio_repository.get_caserio_by_id(caserio_id)
        if not caserio:
            raise NotFoundException("El caserio no existe")

        self.caserio_repository.delete_caserio_by_id(caserio_id)


    def get_all_caserios_by_centro_poblado_id(self, centro_poblado_id: int | None) -> List[CaserioResponseWithCentroPobladoId]:
        caserios = self.caserio_repository.get_all_caserios_by_centro_poblado_id(centro_poblado_id)

        return [
            CaserioResponseWithCentroPobladoId(
                id=caserio.id,
                nombre_caserio=caserio.nombre_caserio,
                centro_poblado_id=caserio.centro_poblado_id
            ) for caserio in caserios
        ]


    def find_by_string(self, search_string: str) -> List[CaserioResponseDTO]:
        caserios = self.caserio_repository.find_by_string(search_string)

        if not caserios:
            raise NotFoundException("No se encontraron caserios")

        return [
            CaserioResponseDTO(
                id=caserio['id'],
                nombre_caserio=caserio['nombre_caserio'],
                centro_poblado_nombre=caserio['nombre_centro_poblado']
            ) for caserio in caserios
        ]


    def get_all_caserios_by_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        return self.caserio_repository.get_all_paginated(page, page_size)


    def get_caserio_by_id(self, caserio_id: int) -> Optional[CaserioResponseWithCentroPobladoId]:
        caserio = self.caserio_repository.get_caserio_by_id(caserio_id)
        if not caserio:
            raise NotFoundException("El caserio no existe")

        return CaserioResponseWithCentroPobladoId(
            id=caserio.id,
            nombre_caserio=caserio.nombre_caserio,
            centro_poblado_id=caserio.centro_poblado_id
        )