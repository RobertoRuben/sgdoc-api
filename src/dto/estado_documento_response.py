from pydantic import BaseModel
from datetime import datetime

class EstadoDocumentoResponse(BaseModel):
    id: int
    estado: str
    fecha: datetime
    comentario: str
