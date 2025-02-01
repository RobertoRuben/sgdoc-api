from pydantic import BaseModel
from datetime import datetime

class DetalleDerivacionResponse(BaseModel):
    id: int
    estado: str
    comentario: str | None
    fecha: datetime
    recepcionada: bool | None
    usuario_id: int | None