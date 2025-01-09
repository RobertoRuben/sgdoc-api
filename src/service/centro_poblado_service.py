from typing import List, Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.centro_poblado import CentroPoblado
from src.dto.centro_poblado_request import CentroPobladoRequest
from src.dto.centro_poblado_response import CentroPobladoResponse
from src.repository.centro_poblado_repository import CentroPobladoRepository

class CentroPobladoService:

    def __init__(self, centro_poblado_repository: CentroPobladoRepository = Depends()):
        self.centro_poblado_repository = centro_poblado_repository


    def add_centro_poblado(self, centro_poblado_request: CentroPobladoRequest) -> CentroPobladoResponse:
        if self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado):
            raise HTTPException(status_code=400, detail="El centro poblado ya existe en la base de datos")

        new_centro_poblado = CentroPoblado(
            nombre_centro_poblado = centro_poblado_request.nombre_centro_poblado
        )

        created_centro_poblado = self.centro_poblado_repository.add_centro_poblado(new_centro_poblado)

        return CentroPobladoResponse(
            id=created_centro_poblado.id,
            nombre_centro_poblado=created_centro_poblado.nombre_centro_poblado
        )


    def get_all_centros_poblados(self) -> List[CentroPobladoResponse]:
        centros_poblados = self.centro_poblado_repository.get_all()

        return [CentroPobladoResponse(
            id=centro_poblado.id,
            nombre_centro_poblado=centro_poblado.nombre_centro_poblado
        ) for centro_poblado in centros_poblados]


    def update_centro_poblado(self, centro_poblado_id: int, centro_poblado_request: CentroPobladoRequest) -> CentroPobladoResponse:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise HTTPException(status_code=404, detail="Centro poblado no encontrado")

        if self.centro_poblado_repository.exist(centro_poblado_request.nombre_centro_poblado):
            raise HTTPException(status_code=400, detail="El nombre del centro poblado ya existe en la base de datos")

        centro_poblado.nombre_centro_poblado = centro_poblado_request.nombre_centro_poblado

        updated_centro_poblado = self.centro_poblado_repository.update_centro_poblado(centro_poblado)

        return CentroPobladoResponse(
            id=updated_centro_poblado.id,
            nombre_centro_poblado=updated_centro_poblado.nombre_centro_poblado
        )


    def delete_centro_poblado_by_id(self, centro_poblado_id: int) -> None:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise HTTPException(status_code=404, detail="Centro poblado no encontrado")

        self.centro_poblado_repository.delete_by_id(centro_poblado_id)


    def find_centro_poblado_by_string(self, search_string: str) -> List[CentroPobladoResponse]:
        centros_poblados = self.centro_poblado_repository.find_by_string(search_string)

        if not centros_poblados:
            raise HTTPException(status_code=404, detail="Centro poblado no encontrado")

        return [CentroPobladoResponse(
            id=centro_poblado.id,
            nombre_centro_poblado=centro_poblado.nombre_centro_poblado
        ) for centro_poblado in centros_poblados]


    def get_all_centros_poblados_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        return self.centro_poblado_repository.get_all_pagination(page, page_size)


    def get_centro_poblado_by_id(self, centro_poblado_id: int) -> CentroPobladoResponse:
        centro_poblado = self.centro_poblado_repository.get_by_id(centro_poblado_id)

        if not centro_poblado:
            raise HTTPException(status_code=404, detail="Centro poblado no encontrado")

        return CentroPobladoResponse(
            id=centro_poblado.id,
            nombre_centro_poblado=centro_poblado.nombre_centro_poblado
        )
