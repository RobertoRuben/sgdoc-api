from typing import List, Dict, Any
from fastapi import Depends
from src.exception import NotFoundException, ConflictException
from src.model.entity.centro_poblado import CentroPoblado
from src.dto.centro_poblado_request_dto import CentroPobladoRequestDTO
from src.dto.centro_poblado_response_dto import CentroPobladoResponseDTO
from src.repository.centro_poblado_repository import CentroPobladoRepository

class CentroPobladoService:

    def __init__(self, centro_poblado_repository: CentroPobladoRepository = Depends()):
        self.centro_poblado_repository = centro_poblado_repository


    def add_centro_poblado(self, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        if self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado):
            raise ConflictException("El centro poblado ya existe en la base de datos")

        new_centro_poblado = CentroPoblado(
            nombre_centro_poblado = centro_poblado_request.nombre_centro_poblado
        )

        created_centro_poblado = self.centro_poblado_repository.add_centro_poblado(new_centro_poblado)

        return CentroPobladoResponseDTO(
            id=created_centro_poblado.id,
            nombre_centro_poblado=created_centro_poblado.nombre_centro_poblado
        )


    def get_all_centros_poblados(self) -> List[CentroPobladoResponseDTO]:
        centros_poblados = self.centro_poblado_repository.get_all()

        return [
            CentroPobladoResponseDTO(
                id=centro_poblado.id,
                nombre_centro_poblado=centro_poblado.nombre_centro_poblado
            ) for centro_poblado in centros_poblados
        ]


    def update_centro_poblado(self, centro_poblado_id: int, centro_poblado_request: CentroPobladoRequestDTO) -> CentroPobladoResponseDTO:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise NotFoundException("Centro poblado no encontrado")

        if centro_poblado.nombre_centro_poblado == centro_poblado_request.nombre_centro_poblado:
            return CentroPobladoResponseDTO(
                id=centro_poblado.id,
                nombre_centro_poblado=centro_poblado.nombre_centro_poblado
            )

        if self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado):
            raise ConflictException("El centro poblado ya existe en la base de datos")

        centro_poblado.nombre_centro_poblado = centro_poblado_request.nombre_centro_poblado

        updated_centro_poblado = self.centro_poblado_repository.update_centro_poblado(centro_poblado)

        return CentroPobladoResponseDTO(
            id=updated_centro_poblado.id,
            nombre_centro_poblado=updated_centro_poblado.nombre_centro_poblado
        )


    def delete_centro_poblado_by_id(self, centro_poblado_id: int) -> None:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise NotFoundException("Centro poblado no encontrado")

        self.centro_poblado_repository.delete_by_id(centro_poblado_id)


    def find_centro_poblado_by_string(self, search_string: str) -> List[CentroPobladoResponseDTO]:
        centros_poblados = self.centro_poblado_repository.find_by_string(search_string)

        if not centros_poblados:
            raise NotFoundException("Centro poblado no encontrado")

        return [
            CentroPobladoResponseDTO(
                id=centro_poblado.id,
                nombre_centro_poblado=centro_poblado.nombre_centro_poblado
            ) for centro_poblado in centros_poblados
        ]


    def get_all_centros_poblados_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        return self.centro_poblado_repository.get_all_paginated(page, page_size)


    def get_centro_poblado_by_id(self, centro_poblado_id: int) -> CentroPobladoResponseDTO:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise NotFoundException("Centro poblado no encontrado")

        return CentroPobladoResponseDTO(
            id=centro_poblado.id,
            nombre_centro_poblado=centro_poblado.nombre_centro_poblado
        )
