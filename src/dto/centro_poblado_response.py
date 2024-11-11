from pydantic import BaseModel

class CentroPobladoResponse(BaseModel):
    id: int
    nombre_centro_poblado: str
