from pydantic import BaseModel
from datetime import datetime

class DerivacionResponse(BaseModel):
    id: int
    fecha: datetime
    area_origen_id: int
    area_destino_id: int
    documento_id: int