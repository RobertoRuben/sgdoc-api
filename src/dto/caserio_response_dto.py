from pydantic import BaseModel

class CaserioResponseDTO(BaseModel):
    id: int
    nombre_caserio: str
    centro_poblado_id: int | None = None
    nombre_centro_poblado: str | None = None
