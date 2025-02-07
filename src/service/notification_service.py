from abc import ABC, abstractmethod
from typing import List
from src.dto import NotificacionRequestDTO, NotificacionResponseDTO

class NotificationService(ABC):
    @abstractmethod
    async def add_notificacion(self, notificacion_request: NotificacionRequestDTO) -> NotificacionResponseDTO:
        pass

    @abstractmethod
    async def get_all_notificaciones_by_area_id(self, area_id: int) -> List[NotificacionResponseDTO]:
        pass

    @abstractmethod
    async def mark_notification_as_read(self, notificacion_id: int) -> NotificacionResponseDTO:
        pass
