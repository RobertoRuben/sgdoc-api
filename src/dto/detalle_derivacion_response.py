from pydantic import  BaseModel
from datetime import datetime

class DetalleDerivacionResponse(BaseModel):
    id: int
    estado: str
    comentario: str | None
    fecha:datetime
    usuario_recepcion_id: int | None
