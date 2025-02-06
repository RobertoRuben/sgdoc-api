from typing import List, Dict, Any
from fastapi import Depends
from src.exception import ConflictException, NotFoundException, InternalServerException
from src.model.entity.ambito import Ambito
from src.dto.ambito_request import AmbitoRequest
from src.dto.ambito_response import AmbitoResponse
from src.repository.ambito_repository import AmbitoRepository

class AmbitoService:
    def __init__(self, ambito_repository: AmbitoRepository = Depends()):
        self.ambito_repository = ambito_repository


    async def add_ambito(self, ambito_request: AmbitoRequest) -> AmbitoResponse:
        try:
            exists = await self.ambito_repository.exists(ambito_request.nombre_ambito)
            if exists:
                raise ConflictException("El ámbito ya existe en la base de datos")

            new_ambito = Ambito(
                nombre_ambito=ambito_request.nombre_ambito
            )
            created_ambito = await self.ambito_repository.add_ambito(new_ambito)

            return AmbitoResponse(
                id=created_ambito.id,
                nombre_ambito=created_ambito.nombre_ambito
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear el ámbito",
                error_details=str(e)
            ) from e


    async def get_all_ambitos(self) -> List[AmbitoResponse]:
        try:
            ambitos = await self.ambito_repository.get_all_ambitos()
            return [
                AmbitoResponse(
                    id=ambito.id,
                    nombre_ambito=ambito.nombre_ambito
                ) for ambito in ambitos
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener los ámbitos",
                error_details=str(e)
            ) from e


    async def update_ambito(self, ambito_id: int, ambito_request: AmbitoRequest) -> AmbitoResponse:
        try:
            ambito = await self.ambito_repository.get_ambito_by_id(ambito_id)
            if not ambito:
                raise NotFoundException("Ámbito no encontrado")

            if ambito.nombre_ambito == ambito_request.nombre_ambito:
                return AmbitoResponse(
                    id=ambito.id,
                    nombre_ambito=ambito.nombre_ambito
                )

            exists = await self.ambito_repository.exists(ambito_request.nombre_ambito)
            if exists:
                raise ConflictException("El ámbito ya existe en la base de datos")

            ambito.nombre_ambito = ambito_request.nombre_ambito
            updated_ambito = await self.ambito_repository.update_ambito(ambito)

            return AmbitoResponse(
                id=updated_ambito.id,
                nombre_ambito=updated_ambito.nombre_ambito
            )
        except (ConflictException, NotFoundException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar el ámbito",
                error_details=str(e)
            ) from e


    async def delete_ambito(self, ambito_id: int) -> None:
        try:
            ambito = await self.ambito_repository.get_ambito_by_id(ambito_id)
            if not ambito:
                raise NotFoundException("Ámbito no encontrado")

            await self.ambito_repository.delete_ambito_by_id(ambito_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar el ámbito",
                error_details=str(e)
            ) from e


    async def find_ambito(self, search_string: str) -> List[AmbitoResponse]:
        try:
            ambitos = await self.ambito_repository.find_by_string(search_string)
            return [
                AmbitoResponse(
                    id=ambito.id,
                    nombre_ambito=ambito.nombre_ambito
                ) for ambito in ambitos
            ]
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al buscar ámbitos",
                error_details=str(e)
            ) from e


    async def get_ambitos_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        try:
            return await self.ambito_repository.get_all_paginated(page, page_size)
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener ámbitos paginados",
                error_details=str(e)
            ) from e


    async def get_ambito_by_id(self, ambito_id: int) -> AmbitoResponse:
        try:
            ambito = await self.ambito_repository.get_ambito_by_id(ambito_id)
            if not ambito:
                raise NotFoundException("Ámbito no encontrado")

            return AmbitoResponse(
                id=ambito.id,
                nombre_ambito=ambito.nombre_ambito
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener el ámbito",
                error_details=str(e)
            ) from e
