from pydantic import BaseModel

class CentroPobladoResponseDTO(BaseModel):
    id: int
    nombre_centro_poblado: str
