from pydantic import  BaseModel
from datetime import datetime

class DetalleDerivacionDetailsResponse(BaseModel):
    id: int
    estado: str
    comentario: str | None
    fecha: datetime
    recepcionada: bool | None
    usuario_id: int | None
    nombre_usuario: str | None
