from typing import List, Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.ambito import Ambito
from src.dto.ambito_request import AmbitoRequest
from src.dto.ambito_response import AmbitoResponse
from src.repository.ambito_repository import AmbitoRepository

class AmbitoService:

    def __init__(self, ambito_repository: AmbitoRepository = Depends()):
        self.ambito_repository = ambito_repository


    def add_amibito(self, ambito_request: AmbitoRequest) -> AmbitoResponse:
        if self.ambito_repository.exists(ambito_request.nombre_ambito):
            raise HTTPException(status_code=400, detail="El ambito ya existe en la base de datos")

        new_ambito = Ambito(
            nombre_ambito=ambito_request.nombre_ambito
        )

        created_ambito = self.ambito_repository.add_ambito(new_ambito)

        return AmbitoResponse(
            id=created_ambito.id,
            nombre_ambito=created_ambito.nombre_ambito
        )


    def get_all_ambitos(self) -> List[AmbitoResponse]:
        ambitos = self.ambito_repository.get_all_ambient()

        return [AmbitoResponse(
            id=ambito.id,
            nombre_ambito=ambito.nombre_ambito
        ) for ambito in ambitos]


    def update_ambito(self, ambito_id: int, ambito_request: AmbitoRequest) -> AmbitoResponse:
        ambito = self.ambito_repository.get_ambito_by_id(ambito_id)

        if not ambito:
            raise HTTPException(status_code=404, detail="Ambito no encontrado")

        if self.ambito_repository.exists(ambito_request.nombre_ambito):
            raise HTTPException(status_code=400, detail="El ambito ya existe en la base de datos")

        ambito.nombre_ambito = ambito_request.nombre_ambito

        updated_ambito = self.ambito_repository.update_ambito(ambito)

        return AmbitoResponse(
            id=updated_ambito.id,
            nombre_ambito=updated_ambito.nombre_ambito
        )


    def delete_ambito(self, ambito_id: int):
        ambito = self.ambito_repository.get_ambito_by_id(ambito_id)

        if not ambito:
            raise HTTPException(status_code=404, detail="Ambito no encontrado")

        self.ambito_repository.delete_ambito_by_id(ambito_id)


    def find_ambito_by_string(self, search_string: str) -> List[AmbitoResponse]:
        ambitos = self.ambito_repository.find_by_string(search_string)

        return [AmbitoResponse(
            id=ambito.id,
            nombre_ambito=ambito.nombre_ambito
        ) for ambito in ambitos]


    def get_ambitos_by_pagination(self, page: int, page_size: int) ->Dict[str, Any]:
        return self.ambito_repository.get_all_pagination(page, page_size)