from typing import List
from fastapi import Depends, APIRouter
from src.websocket.manager import manager
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto.notificacion_response_dto import NotificacionResponseDTO
from src.dto.notificacion_request_dto import NotificacionRequestDTO
from src.service.notificacion_service import NotificacionService

router = APIRouter(tags=["Notificaciones"])

notificaciones_tag_metadata = {
    "name": "Notificaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Notificacion, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de notificaciones.",
}


@router.post(
    "/notificaciones",
    response_model=NotificacionResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        401: {"description": "No autorizado", "model": NotAuthenticatedResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Crea una nueva notificación"
)
async def add_notificacion(notificacion_request: NotificacionRequestDTO, service: NotificacionService = Depends()):
    result = service.add_notificacion(notificacion_request)

    await manager.notify_area(
        result.area_destino_id,
        {
            "type": "NUEVA_NOTIFICACION",
            "data": {
                "id": result.id,
                "comentario": result.comentario,
                "leido": result.leido,
                "fecha_creacion": str(result.fecha_creacion)
            }
        }
    )

    return result


@router.get(
    "/notificaciones/area/{area_id}",
    response_model=List[NotificacionResponseDTO],
    responses = {
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "El área no existe", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las notificaciones de un área"
)
async def get_notificaciones_by_area_id(area_id: int, service: NotificacionService = Depends()):
    return service.get_notificaciones_by_area(area_id)


@router.put(
    "/notificaciones/{notificacion_id}/leida",
    response_model=NotificacionResponseDTO,
    responses={
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "La notifcacion no existe", "model": ErrorResponseSchema},
        409: {"description": "Conflicto - El recurso ya existe", "model": ErrorResponseSchema},
        422: {"description": "Error de validación", "model": ValidationErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Marca una notificación como leída"
)
async def mark_notification_as_read(notificacion_id: int, service: NotificacionService = Depends()):
    return service.mark_notification_as_read(notificacion_id)