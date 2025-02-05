from typing import List
from fastapi import Depends

from src.exception import NotFoundException
from src.dto.notificacion_request_dto import NotificacionRequestDTO
from src.dto.notificacion_response_dto import NotificacionResponseDTO
from src.model.entity.notifcacion import Notificacion
from src.repository.notificacion_repository import NotificacionRepository
from src.repository.area_repository import AreaRepository

class NotificacionService:
    def __init__(
        self,
        notificacion_repository: NotificacionRepository = Depends(),
        area_repository: AreaRepository = Depends()
    ):
        self.notificacion_repository = notificacion_repository
        self.area_repository = area_repository


    def add_notificacion(self, notificacion_request: NotificacionRequestDTO) -> NotificacionResponseDTO:
        if not self.area_repository.exists_by_id(notificacion_request.area_destino_id):
            raise NotFoundException("El área de destino no existe")

        notificacion = Notificacion(
            comentario=notificacion_request.comentario,
            area_destino_id=notificacion_request.area_destino_id
        )
        notificacion = self.notificacion_repository.add_notificacion(notificacion)
        return NotificacionResponseDTO(
            id=notificacion.id,
            comentario=notificacion.comentario,
            area_destino_id=notificacion.area_destino_id,
            leido=notificacion.leido,
            fecha_creacion=notificacion.fecha_creacion
        )


    def get_notificaciones_by_area(self, area_id: int) -> List[NotificacionResponseDTO]:
        if not self.area_repository.exists_by_id(area_id):
            raise NotFoundException(f"El área {area_id} no existe")

        notificaciones = self.notificacion_repository.get_notificaciones_by_area_destino_id(area_id)

        return [
            NotificacionResponseDTO(
                id=n.id,
                comentario=n.comentario,
                area_destino_id=n.area_destino_id,
                leido=n.leido,
                fecha_creacion=n.fecha_creacion
            )
            for n in notificaciones
        ]


    def mark_notification_as_read(self, notificacion_id: int) -> NotificacionResponseDTO:
        if not self.notificacion_repository.exists_by_id(notificacion_id):
            raise NotFoundException(f"La notificación {notificacion_id} no existe")

        notificacion = self.notificacion_repository.mark_notification_as_read(notificacion_id)
        if notificacion is None:
            raise NotFoundException("La notificación no existe")

        return NotificacionResponseDTO(
            id=notificacion.id,
            comentario=notificacion.comentario,
            area_destino_id=notificacion.area_destino_id,
            leido=notificacion.leido,
            fecha_creacion=notificacion.fecha_creacion
        )
