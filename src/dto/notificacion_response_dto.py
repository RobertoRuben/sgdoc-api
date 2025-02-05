from pydantic import BaseModel
from datetime import datetime

class NotificacionResponseDTO(BaseModel):
    id: int
    comentario: str
    area_destino_id: int
    leido: bool
    fecha_creacion: datetime