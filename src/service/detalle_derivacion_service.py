from typing import List
from fastapi import HTTPException, Depends
from src.dto.detalle_derivacion_request import DetalleDerivacionRequest
from src.dto.detalle_derivacion_response import DetalleDerivacionResponse
from src.model.enum.estado_derivacion_enum import EstadoDerivacionEnum
from src.model.entity.detalle_derivacion import DetalleDerivacion
from src.repository.derivacion_repository import DerivacionRepository
from src.repository.usuario_repository import UsuarioRepository
from src.repository.detalle_derivacion_repository import DetalleDerivacionRepository


class DetalleDerivacionService:
    def __init__(self, derivacion_repository: DerivacionRepository = Depends(),
                 usuario_repository: UsuarioRepository = Depends(),
                 detalle_derivacion_repository: DetalleDerivacionRepository = Depends()):

        self.derivacion_repository = derivacion_repository
        self.usuario_repository = usuario_repository
        self.detalle_derivacion_repository = detalle_derivacion_repository

    def add_detalle_derivacion(self, derivacion_request: DetalleDerivacionRequest) -> DetalleDerivacionResponse:
        # Validar existencia de la derivación
        if not self.derivacion_repository.exists_by_id(derivacion_request.derivacion_id):
            raise HTTPException(status_code=404, detail="No existe una derivación con ese ID")

        # Validar existencia del usuario
        if not self.usuario_repository.exists_by_id(derivacion_request.usuario_recepcion_id):
            raise HTTPException(status_code=404, detail="No existe un usuario con ese ID")

        # Mejorar la validación para incluir tanto None como string vacío
        if derivacion_request.estado == EstadoDerivacionEnum.recepcionada and (derivacion_request.comentario is None or derivacion_request.comentario.strip() == ""):
            derivacion_request.comentario = f"La derivación ha sido recepcionada por el área destino por el usuario {derivacion_request.usuario_recepcion_id}"

        # Crear nueva entidad
        new_detalle_derivacion = DetalleDerivacion(
            estado=derivacion_request.estado,
            comentario=derivacion_request.comentario,
            usuario_recepcion_id=derivacion_request.usuario_recepcion_id,
            derivacion_id=derivacion_request.derivacion_id,
        )

        # Persistir en base de datos
        created_detalle_derivacion = self.detalle_derivacion_repository.add_detalle_derivacion(new_detalle_derivacion)

        # Retornar respuesta
        return DetalleDerivacionResponse(
            id=created_detalle_derivacion.id,
            estado=created_detalle_derivacion.estado,
            comentario=created_detalle_derivacion.comentario,
            fecha=created_detalle_derivacion.fecha,
            usuario_recepcion_id=created_detalle_derivacion.usuario_recepcion_id,
        )


    def get_all_detalle_derivacion_by_id(self, derivacion_id: int) -> List[DetalleDerivacionResponse]:

        detalles_derivacion = self.detalle_derivacion_repository.get_all_by_derivacion_id(derivacion_id)

        return [
            DetalleDerivacionResponse(
                id=detalle.id,
                estado=detalle.estado,
                comentario=detalle.comentario,
                fecha=detalle.fecha,
                usuario_recepcion_id=detalle.usuario_recepcion_id
            )
            for detalle in detalles_derivacion
        ]


    def update_detalle_derivacion(self, detalle_derivacion_id: int, detalle_derivacion_request: DetalleDerivacionRequest) -> DetalleDerivacionResponse:
        # Validar existencia de la derivación

        if not self.derivacion_repository.exists_by_id(detalle_derivacion_request.derivacion_id):
            raise HTTPException(status_code=404, detail="No existe una derivación con ese ID")

        if not self.detalle_derivacion_repository.exists_detalle_derivacion_by_id(detalle_derivacion_id):
            raise HTTPException(status_code=404, detail="No existe un detalle de derivacion con ese id")

        # Validar existencia del usuario
        if not self.usuario_repository.exists_by_id(detalle_derivacion_request.usuario_recepcion_id):
            raise HTTPException(status_code=404, detail="No existe un usuario con ese ID")

        # Mejorar la validación para incluir tanto None como string vacío
        if detalle_derivacion_request.estado == EstadoDerivacionEnum.recepcionada and (detalle_derivacion_request.comentario is None or detalle_derivacion_request.comentario.strip() == ""):
            detalle_derivacion_request.comentario = f"La derivación ha sido recepcionada por el área destino por el usuario {detalle_derivacion_request.usuario_recepcion_id}"

        # Obtener entidad existente
        detalle_derivacion = self.detalle_derivacion_repository.get_by_id(detalle_derivacion_id)

        # Actualizar entidad
        detalle_derivacion.estado = detalle_derivacion_request.estado
        detalle_derivacion.comentario = detalle_derivacion_request.comentario
        detalle_derivacion.usuario_recepcion_id = detalle_derivacion_request.usuario_recepcion_id

        # Persistir en base de datos
        updated_detalle_derivacion = self.detalle_derivacion_repository.update_detalle_derivacion(detalle_derivacion)

        # Retornar respuesta
        return DetalleDerivacionResponse(
            id=updated_detalle_derivacion.id,
            estado=updated_detalle_derivacion.estado,
            comentario=updated_detalle_derivacion.comentario,
            fecha=updated_detalle_derivacion.fecha,
            usuario_recepcion_id=updated_detalle_derivacion.usuario_recepcion_id,
        )


    def delete_detalle_derivacion_by_id(self, detalle_derivacion_id: int) -> None:
        if not self.detalle_derivacion_repository.exists_detalle_derivacion_by_id(detalle_derivacion_id):
            raise HTTPException(status_code=404, detail="No existe un detalle de derivacion con ese id")
        self.detalle_derivacion_repository.delete_by_id(detalle_derivacion_id)
        return None



