from typing import List,  Dict, Any
from fastapi import HTTPException, Depends
from src.model.entity.rol import Rol
from src.dto.rol_request import RolRequest
from src.dto.rol_response import RolReponse
from src.repository.rol_repository import RolRepository

class RolService:

    def __init__(self, rol_repository: RolRepository = Depends()):
        self.rol_repository = rol_repository


    def add_rol(self, rol_request: RolRequest) -> RolReponse:
        if self.rol_repository.exists(rol_request.nombre_rol):
            raise HTTPException(status_code=400, detail="El rol ya existe en la base de datos")

        new_rol = Rol(
            nombre_rol = rol_request.nombre_rol
        )

        created_rol = self.rol_repository.add_rol(new_rol)

        return RolReponse(
            id=created_rol.id,
            nombre_rol=created_rol.nombre_rol
        )


    def get_roles(self) -> List[RolReponse]:
        roles = self.rol_repository.get_all()

        return [RolReponse(
            id=rol.id,
            nombre_rol=rol.nombre_rol
        ) for rol in roles]


    def update_rol(self, rol_id: int, rol_request: RolRequest) -> RolReponse:
        rol = self.rol_repository.get_by_id(rol_id)

        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        if self.rol_repository.exists(rol_request.nombre_rol):
            raise HTTPException(status_code=400, detail="El rol ya existe en la base de datos")

        rol.nombre_rol = rol_request.nombre_rol

        rol = self.rol_repository.update_rol(rol)

        return RolReponse(
            id=rol.id,
            nombre_rol=rol.nombre_rol
        )


    def delete_rol(self, rol_id: int) -> None:
        rol = self.rol_repository.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        self.rol_repository.delete_by_id(rol_id)


    def find_rol_by_string(self, search_string: str) -> List[RolReponse]:
        roles = self.rol_repository.find_by_string(search_string)

        if not roles:
            raise HTTPException(status_code=404, detail="No se encontro el rol que buscaba")

        return [RolReponse(
            id=rol.id,
            nombre_rol=rol.nombre_rol
        ) for rol in roles]


    def get_roles_with_pagination(self, page: int, page_size:int) -> Dict[str, Any]:
        return self.rol_repository.get_all_pagination(page, page_size)


    def get_rol_id(self, rol_id: int) -> RolReponse:
        rol = self.rol_repository.get_by_id(rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return RolReponse(
            id=rol.id,
            nombre_rol=rol.nombre_rol
        )


