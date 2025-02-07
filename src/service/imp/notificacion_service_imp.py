from typing import List
from fastapi import Depends
from src.exception import NotFoundException, ConflictException, InternalServerException
from src.repository import NotificacionRepository, AreaRepository
from src.model.entity.notifcacion import Notificacion
from src.dto import NotificacionRequestDTO, NotificacionResponseDTO
from src.service import NotificationService


class NotificacionServiceImp(NotificationService):
    def __init__(
        self,
        notificacion_repository: NotificacionRepository = Depends(),
        area_repository: AreaRepository = Depends()
    ):
        self.notificacion_repository = notificacion_repository
        self.area_repository = area_repository


    async def add_notificacion(self, notificacion_request: NotificacionRequestDTO) -> NotificacionResponseDTO:
        try:
            exists_area = await self.area_repository.exists_by_id(notificacion_request.area_destino_id)
            if not exists_area:
                raise NotFoundException("El área de destino no existe")

            notificacion = Notificacion(
                comentario=notificacion_request.comentario,
                area_destino_id=notificacion_request.area_destino_id
            )
            created_notificacion = await self.notificacion_repository.add_notificacion(notificacion)

            return NotificacionResponseDTO(
                id=created_notificacion.id,
                comentario=created_notificacion.comentario,
                area_destino_id=created_notificacion.area_destino_id,
                leido=created_notificacion.leido,
                fecha_creacion=created_notificacion.fecha_creacion
            )
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al crear la notificación",
                error_details=str(e)
            ) from e


    async def get_all_notificaciones_by_area_id(self, area_id: int) -> List[NotificacionResponseDTO]:
        try:
            exists_area = await self.area_repository.exists_by_id(area_id)
            if not exists_area:
                raise NotFoundException(f"El área {area_id} no existe")

            notificaciones = await self.notificacion_repository.get_notificaciones_by_area_destino_id(area_id)
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
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al obtener las notificaciones",
                error_details=str(e)
            ) from e


    async def mark_notification_as_read(self, notificacion_id: int) -> NotificacionResponseDTO:
        try:
            exists = await self.notificacion_repository.exists_by_id(notificacion_id)
            if not exists:
                raise NotFoundException(f"La notificación {notificacion_id} no existe")

            notificacion = await self.notificacion_repository.mark_notification_as_read(notificacion_id)
            if not notificacion:
                raise NotFoundException("La notificación no existe")

            return NotificacionResponseDTO(
                id=notificacion.id,
                comentario=notificacion.comentario,
                area_destino_id=notificacion.area_destino_id,
                leido=notificacion.leido,
                fecha_creacion=notificacion.fecha_creacion
            )
        except (NotFoundException, ConflictException) as e:
            raise e
        except Exception as e:
            raise InternalServerException(
                detail="Error interno al actualizar la notificación",
                error_details=str(e)
            ) from e
