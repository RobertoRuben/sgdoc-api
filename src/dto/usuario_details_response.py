from pydantic import BaseModel
from datetime import datetime

class UsuarioDetailsResponse(BaseModel):
    id: int
    nombre_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None
    is_active: bool
    rol_nombre: str
    trabajador_nombre: str