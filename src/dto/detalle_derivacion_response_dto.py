from pydantic import BaseModel
from datetime import datetime

class DetalleDerivacionResponseDTO(BaseModel):
    id: int
    estado: str
    comentario: str | None = None
    fecha: datetime | None = None
    recepcionada: bool | None = None
    usuario_id: int | None = None
    nombre_usuario: str | None = None