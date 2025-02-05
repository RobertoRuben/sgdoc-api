from pydantic import BaseModel

class NotificacionRequestDTO(BaseModel):
    comentario: str
    area_destino_id: int