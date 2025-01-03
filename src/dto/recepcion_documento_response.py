from pydantic import BaseModel
from datetime import datetime

class RecepcionDocumentoResponse(BaseModel):
    id: int
    documento_id: int
    usuario_id: int
    fecha_recepcion: datetime