from typing import List, Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.remitente import Remitente
from src.dto.remitente_request import RemitenteRequest
from src.dto.remitente_response import RemitenteResponse
from src.repository.remitente_repository import RemitenteRepository


class RemitenteService:

    def __init__(self, remitente_repository: RemitenteRepository = Depends()):
        self.remitente_repository = remitente_repository

    def add_remitente(self, remitente_request: RemitenteRequest) -> RemitenteResponse:
        if self.remitente_repository.exists(remitente_request.dni):
            raise HTTPException(status_code=400, detail="El remitente ya existe en la base de datos")

        new_remitente = Remitente(
            dni = remitente_request.dni,
            nombres= remitente_request.nombres,
            apellido_paterno=remitente_request.apellido_paterno,
            apellido_materno= remitente_request.apellido_materno,
            genero= remitente_request.genero
        )

        created_remitente = self.remitente_repository.add_remitentes(new_remitente)

        return RemitenteResponse(
            id=created_remitente.id,
            dni=created_remitente.dni,
            nombres=created_remitente.nombres,
            apellido_paterno=created_remitente.apellido_paterno,
            apellido_materno=created_remitente.apellido_materno,
            genero=created_remitente.genero
        )


    def get_remitentes(self) -> List[RemitenteResponse]:
        remitentes = self.remitente_repository.get_all()

        return [RemitenteResponse(
            id=remitente.id,
            dni=remitente.dni,
            nombres=remitente.nombres,
            apellido_paterno=remitente.apellido_paterno,
            apellido_materno=remitente.apellido_materno,
            genero=remitente.genero
        ) for remitente in remitentes]


    def update_remitente(self, remitente_id: int, remitente_request: RemitenteRequest) -> RemitenteResponse:
        remitente = self.remitente_repository.get_by_id(remitente_id)

        if not remitente:
            raise HTTPException(status_code=404, detail="Remitente no encontrado")

        if self.remitente_repository.exists(remitente_request.dni):
            raise HTTPException(status_code=400, detail="El DNI ya existe en la base de datos")

        remitente.dni = remitente_request.dni
        remitente.nombres = remitente_request.nombres
        remitente.apellido_paterno = remitente_request.apellido_paterno
        remitente.apellido_materno = remitente_request.apellido_materno
        remitente.genero = remitente_request.genero

        updated_remitente = self.remitente_repository.update_remitente(remitente)

        return RemitenteResponse(
            id=updated_remitente.id,
            dni=updated_remitente.dni,
            nombres=updated_remitente.nombres,
            apellido_paterno=updated_remitente.apellido_paterno,
            apellido_materno=updated_remitente.apellido_materno,
            genero=updated_remitente.genero
        )


    def delete_remitente(self, remitente_id: int) -> None:
        remitente = self.remitente_repository.get_by_id(remitente_id)
        if not remitente:
            raise HTTPException(status_code=404, detail="Remitente no encontrado")

        self.remitente_repository.delete_by_id(remitente_id)


    def find_remitentes_by_string(self, search_string: str) -> List[RemitenteResponse]:
        remitentes = self.remitente_repository.find_by_string(search_string)
        if not remitentes:
            raise HTTPException(status_code=404, detail="No se encontraron resulatdos que coincidan con su busqueda.")
        return [RemitenteResponse(
            id=remitente.id,
            dni=remitente.dni,
            nombres=remitente.nombres,
            apellido_paterno=remitente.apellido_paterno,
            apellido_materno=remitente.apellido_materno,
            genero=remitente.genero
        ) for remitente in remitentes]


    def get_remitentes_with_pagination(self, page: int, page_size: int) -> Dict[str, Any]:
        return RemitenteRepository.get_all_pagination(page, page_size)
