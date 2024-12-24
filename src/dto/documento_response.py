from datetime import datetime
from pydantic import BaseModel

class DocumentoResponse(BaseModel):
    id: int
    remitente_id: int
    nombre: str
    folios: int
    asunto: str
    ambito_id: int
    categoria_id: int
    caserio_id: int
    centro_poblado_id: int | None
    fecha_ingreso: datetime