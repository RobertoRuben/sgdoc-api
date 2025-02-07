from typing import List
from fastapi import Depends, APIRouter
from src.websocket.manager import manager
from src.schemas import ErrorResponseSchema, ValidationErrorResponseSchema, NotAuthenticatedResponseSchema
from src.dto import NotificacionRequestDTO, NotificacionResponseDTO
from src.service import NotificacionService
from src.service.imp import NotificacionServiceImp

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)

notificaciones_tag_metadata = {
    "name": "Notificaciones",
    "description": "Esta sección proporciona los endpoints para gestionar la entidad de Notificacion, incluyendo la"
                   " creación, recuperación, actualización, eliminación y búsqueda de registros de notificaciones.",
}

def get_notificaction_service_imp(service: NotificacionServiceImp = Depends()) -> NotificacionService:
    return service

@router.post(
    "",
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
async def add_notificacion(
    notificacion_request: NotificacionRequestDTO,
    service: NotificacionService = Depends(get_notificaction_service_imp)
):
    result = await service.add_notificacion(notificacion_request)

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
    "/area/{area_id}",
    response_model=List[NotificacionResponseDTO],
    responses = {
        400: {"description": "Solicitud inválida", "model": ErrorResponseSchema},
        404: {"description": "El área no existe", "model": ErrorResponseSchema},
        500: {"description": "Error interno del servidor", "model": ErrorResponseSchema},
    },
    description="Obtiene todas las notificaciones de un área"
)
async def get_notificaciones_by_area_id(
    area_id: int,
    service: NotificacionService = Depends(get_notificaction_service_imp)
):
    return await service.get_all_notificaciones_by_area_id(area_id)


@router.put(
    "/{notificacion_id}/leida",
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
async def mark_notification_as_read(
    notificacion_id: int,
    service: NotificacionService = Depends(get_notificaction_service_imp)
):
    return await service.mark_notification_as_read(notificacion_id)