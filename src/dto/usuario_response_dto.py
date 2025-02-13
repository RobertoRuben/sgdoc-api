from pydantic import BaseModel
from datetime import datetime

class UsuarioResponseDTO(BaseModel):
    id: int
    nombre_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None = None
    is_active: bool
    rol_id: int | None = None
    rol_nombre: str | None = None
    trabajador_id: int | None = None
    trabajador_nombre: str | None = None
