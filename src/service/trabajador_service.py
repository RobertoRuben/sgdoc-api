from typing import List, Dict, Any, Optional
from fastapi import HTTPException, Depends

from src.dto.trabajador_response import TrabajadorResponse
from src.dto.trabajador_request import TrabajadorRequest
from src.dto.trabajador_simple_response import TrabajadorSimpleReponse
from src.dto.trabajador_detail_response import TrabajadorDetailResponse
from src.model.entity.trabajador import Trabajador
from src.repository.trabajador_repository import TrabajadorRepository

class TrabajadorService:

    def __init__(self, trabajador_repository: TrabajadorRepository = Depends()):
        self.trabajador_repository = trabajador_repository


    def add_trabajador(self, trabajador_request: TrabajadorRequest) -> TrabajadorResponse:

        if self.trabajador_repository.exists_trabajador_by_dni(trabajador_request.dni):
            raise HTTPException(status_code=400, detail="El trabajador ya existe en la base de datos")

        new_trabajador = Trabajador(
            dni=trabajador_request.dni,
            nombres=trabajador_request.nombres,
            apellido_paterno=trabajador_request.apellido_paterno,
            apellido_materno=trabajador_request.apellido_materno,
            genero=trabajador_request.genero,
            area_id=trabajador_request.area_id,
        )

        created_trabajador = self.trabajador_repository.add_trabajador(new_trabajador)

        return TrabajadorResponse(
            id=created_trabajador.id,
            dni=created_trabajador.dni,
            nombres=created_trabajador.nombres,
            apellido_paterno=created_trabajador.apellido_paterno,
            apellido_materno=created_trabajador.apellido_materno,
            genero=created_trabajador.genero,
            area_id=created_trabajador.area_id
        )


    def get_all_id_and_trabajador_name(self) -> List[TrabajadorSimpleReponse]:
        trabajadores = self.trabajador_repository.get_all_id_and_name()
        return [
            TrabajadorSimpleReponse(
                id=trabajador["id"],
                nombres=trabajador["nombres"]
            )
            for trabajador in trabajadores
        ]


    def get_all_trabajadores_by_pagination(self, page:int, page_size:int) -> Dict[str, Any]:
        trabajadores_data = self.trabajador_repository.get_trabajadores_with_area_pagination(page, page_size)
        return trabajadores_data


    def update_trabajador(self, trabajador_id: int, trabajador_request: TrabajadorRequest) -> TrabajadorResponse:
        trabajador = self.trabajador_repository.get_by_id(trabajador_id)

        if not trabajador:
            raise HTTPException(status_code=404, detail="El trabajador no existe en la base de datos")

        if self.trabajador_repository.exists_trabajador_by_dni(trabajador_request.dni):
            raise HTTPException(status_code=400, detail="El trabajador ya existe en la base de datos")

        trabajador.dni = trabajador_request.dni
        trabajador.nombres = trabajador_request.nombres
        trabajador.apellido_paterno = trabajador_request.apellido_paterno
        trabajador.apellido_materno = trabajador_request.apellido_materno
        trabajador.genero = trabajador_request.genero
        trabajador.area_id = trabajador_request.area_id

        updated_trabajador = self.trabajador_repository.update_trabajador(trabajador)

        return TrabajadorResponse(
            id=updated_trabajador.id,
            dni=updated_trabajador.dni,
            nombres=updated_trabajador.nombres,
            apellido_paterno=updated_trabajador.apellido_paterno,
            apellido_materno=updated_trabajador.apellido_materno,
            genero=updated_trabajador.genero,
            area_id=updated_trabajador.area_id
        )


    def delete_trabajador(self, trabajador_id: int) -> None:
        trabajador = self.trabajador_repository.get_by_id(trabajador_id)

        if not trabajador:
            raise HTTPException(status_code=404, detail="El trabajador no existe en la base de datos")

        self.trabajador_repository.delete_by_id(trabajador_id)


    def find_by_string(self, search_string: str) -> List[TrabajadorDetailResponse]:
        trabajadores = self.trabajador_repository.find_by_string(search_string)

        if not trabajadores:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")

        return [
            TrabajadorDetailResponse(
                id=trabajador['id'],
                dni=trabajador['dni'],
                nombres=trabajador['nombres'],
                apellido_paterno=trabajador['apellido_paterno'],
                apellido_materno=trabajador['apellido_materno'],
                genero=trabajador['genero'],
                nombre_area=trabajador['nombre_area']
            ) for trabajador in trabajadores
        ]


    def get_trabajador_by_id(self, trabajador_id: int) -> Optional[TrabajadorResponse]:
        trabajador = self.trabajador_repository.get_by_id(trabajador_id)

        if not trabajador:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")

        return TrabajadorResponse(
            id=trabajador.id,
            dni=trabajador.dni,
            nombres=trabajador.nombres,
            apellido_paterno=trabajador.apellido_paterno,
            apellido_materno=trabajador.apellido_materno,
            genero=trabajador.genero,
            area_id=trabajador.area_id
        )




