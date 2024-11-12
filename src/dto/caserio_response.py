from pydantic import BaseModel

class CaserioResponse(BaseModel):
    id: int
    nombre_caserio: str
    centro_poblado_nombre: str


class CaserioResponseWithCentroPobladoId(BaseModel):
    id: int
    nombre_caserio: str
    centro_poblado_id: int | None