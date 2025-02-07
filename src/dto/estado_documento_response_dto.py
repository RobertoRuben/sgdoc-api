from pydantic import BaseModel
from datetime import datetime

class EstadoDocumentoResponseDTO(BaseModel):
    id: int
    estado: str
    fecha: datetime
    comentario: str
