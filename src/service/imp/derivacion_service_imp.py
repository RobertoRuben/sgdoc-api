from typing import Dict, Any
from fastapi import Depends
from src.model.entity.derivacion import Derivacion
from src.exception import NotFoundException, InternalServerException
from src.dto import DerivacionRequestDTO, DerivacionResponseDTO
from src.repository import DerivacionRepository, AreaRepository
from src.repository.documento_repository import DocumentoRepository
from src.service import DerivacionService


class DerivacionServiceImp(DerivacionService):
    def __init__(
        self,
        derivacion_repository: DerivacionRepository = Depends(),
        documento_repository: DocumentoRepository = Depends(),
        area_repository: AreaRepository = Depends()
    ):
        self.derivacion_repository = derivacion_repository
        self.documento_repository = documento_repository
        self.area_repository = area_repository


    async def add(self, derivacion_request: DerivacionRequestDTO) -> DerivacionResponseDTO:
        try:
            if not await self.area_repository.exists_by_id(derivacion_request.area_origen_id):
                raise NotFoundException("No existe un área de origen con ese ID")

            if not await self.area_repository.exists_by_id(derivacion_request.area_destino_id):
                raise NotFoundException("No existe un área de destino con ese ID")

            if not await self.documento_repository.exists_by_id(derivacion_request.documento_id):
                raise NotFoundException("No existe un documento con ese ID")

            new_derivacion = Derivacion(
                area_origen_id=derivacion_request.area_origen_id,
                area_destino_id=derivacion_request.area_destino_id,
                documento_id=derivacion_request.documento_id,
                usuario_id=derivacion_request.usuario_id
            )

            created_derivacion = await self.derivacion_repository.add(new_derivacion)

            return DerivacionResponseDTO(
                id=created_derivacion.id,
                fecha=created_derivacion.fecha,
                area_origen_id=created_derivacion.area_origen_id,
                area_destino_id=created_derivacion.area_destino_id,
                documento_id=created_derivacion.documento_id,
                usuario_id=created_derivacion.usuario_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear la derivación",
                error_details=str(e)
            ) from e


    async def get_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        fecha_filtro: str = None,
        estado_filtro: str = None,
        documento_id_filtro: int = None
    ) -> Dict[str, Any]:
        try:
            return await self.derivacion_repository.get_paginated(
                page, page_size, fecha_filtro, estado_filtro, documento_id_filtro
            )
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las derivaciones",
                error_details=str(e)
            ) from e


    async def update(self, derivacion_id: int, derivacion_request: DerivacionRequestDTO) -> DerivacionResponseDTO:
        try:
            derivacion = await self.derivacion_repository.get_by_id(derivacion_id)
            if not derivacion:
                raise NotFoundException("Derivación no encontrada")

            if not await self.area_repository.exists_by_id(derivacion_request.area_origen_id):
                raise NotFoundException("No existe un área de origen con ese ID")

            if not await self.area_repository.exists_by_id(derivacion_request.area_destino_id):
                raise NotFoundException("No existe un área de destino con ese ID")

            if not await self.documento_repository.exists_by_id(derivacion_request.documento_id):
                raise NotFoundException("No existe un documento con ese ID")

            derivacion.area_origen_id = derivacion_request.area_origen_id
            derivacion.area_destino_id = derivacion_request.area_destino_id
            derivacion.documento_id = derivacion_request.documento_id

            updated_derivacion = await self.derivacion_repository.update(derivacion)

            return DerivacionResponseDTO(
                id=updated_derivacion.id,
                fecha=updated_derivacion.fecha,
                area_origen_id=updated_derivacion.area_origen_id,
                area_destino_id=updated_derivacion.area_destino_id,
                documento_id=updated_derivacion.documento_id,
                usuario_id=updated_derivacion.usuario_id
            )
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar la derivación",
                error_details=str(e)
            ) from e


    async def delete_by_id(self, derivacion_id: int) -> None:
        try:
            derivacion = await self.derivacion_repository.get_by_id(derivacion_id)
            if not derivacion:
                raise NotFoundException("Derivación no encontrada")
            await self.derivacion_repository.delete_by_id(derivacion_id)
        except NotFoundException as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al eliminar la derivación",
                error_details=str(e)
            ) from e
