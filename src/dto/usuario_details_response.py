from pydantic import BaseModel
from datetime import datetime

class UsuarioDetailsResponse(BaseModel):
    id: int
    nombre_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None = None
    is_active: bool
    rol_id: int
    rol_nombre: str | None = None
    trabajador_id: int
    trabajador_nombre: str | None = None