from fastapi import HTTPException, Depends
from src.model.entity.derivacion import Derivacion
from src.dto.derivacion_request import DerivacionRequest
from src.dto.derivacion_response import DerivacionResponse
from src.repository.derivacion_repository import DerivacionRepository
from src.repository.documento_repository import DocumentoRepository
from src.repository.area_repository import AreaRepository


class DerivacionService:
    def __init__(self, derivacion_repository: DerivacionRepository = Depends(),
                 documento_repository: DocumentoRepository = Depends(),
                 area_repository: AreaRepository = Depends()):

        self.derivacion_repository = derivacion_repository
        self.documento_repository = documento_repository
        self.area_repository = area_repository

    def add_derivacion(self, derivacion_request: DerivacionRequest) -> DerivacionResponse:

        if not self.area_repository.exists_by_id(derivacion_request.area_origen_id):
            raise HTTPException(status_code=404, detail="No existe un area de origen con ese ID")

        if not self.area_repository.exists_by_id(derivacion_request.area_destino_id):
            raise HTTPException(status_code=404, detail="No existe un area de destino con ese ID")

        if not self.documento_repository.exists_by_id(derivacion_request.documento_id):
            raise HTTPException(status_code=404, detail="No existe un documento con ese ID")

        new_derivacion = Derivacion(
            area_origen_id=derivacion_request.area_origen_id,
            area_destino_id=derivacion_request.area_destino_id,
            documento_id=derivacion_request.documento_id
        )
        created_derivacion = self.derivacion_repository.add(new_derivacion)

        return DerivacionResponse(
            id=created_derivacion.id,
            fecha=created_derivacion.fecha,
            area_origen_id=created_derivacion.area_origen_id,
            area_destino_id=created_derivacion.area_destino_id,
            documento_id=created_derivacion.documento_id
        )

    def update_derivacion(self, derivacion_id: int, derivacion_request: DerivacionRequest) -> DerivacionResponse:
        derivacion = self.derivacion_repository.get_by_id(derivacion_id)

        if not derivacion:
            raise HTTPException(status_code=404, detail="Derivacion no encontrada")

        if not self.area_repository.exists_by_id(derivacion_request.area_origen_id):
            raise HTTPException(status_code=404, detail="No existe un area de origen con ese ID")

        if not self.area_repository.exists_by_id(derivacion_request.area_destino_id):
            raise HTTPException(status_code=404, detail="No existe un area de destino con ese ID")

        if not self.documento_repository.exists_by_id(derivacion_request.documento_id):
            raise HTTPException(status_code=404, detail="No existe un documento con ese ID")

        derivacion.area_origen_id = derivacion_request.area_origen_id
        derivacion.area_destino_id = derivacion_request.area_destino_id
        derivacion.documento_id = derivacion_request.documento_id

        derivacion = self.derivacion_repository.update(derivacion)

        return DerivacionResponse(
            id=derivacion.id,
            fecha=derivacion.fecha,
            area_origen_id=derivacion.area_origen_id,
            area_destino_id=derivacion.area_destino_id,
            documento_id=derivacion.documento_id
        )

    def delete_derivacion(self, derivacion_id: int) -> None:
        derivacion = self.derivacion_repository.get_by_id(derivacion_id)
        if not derivacion:
            raise HTTPException(status_code=404, detail="Derivacion no encontrada")
        self.derivacion_repository.delete_by_id(derivacion_id)
