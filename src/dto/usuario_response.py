from pydantic import BaseModel
from datetime import datetime

class UsuarioResponse(BaseModel):
    id: int
    nombre_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None
    rol_id: int
    trabajador_id: int
    is_active: bool
