from pydantic import BaseModel

class CaserioResponseDTO(BaseModel):
    id: int
    nombre_caserio: str
    centro_poblado_nombre: str | None
    centro_poblado_id: int | None


class CaserioSimpleResponse(BaseModel):
    id: int
    nombre_caserio: str


class CaserioResponseWithCentroPobladoId(BaseModel):
    id: int
    nombre_caserio: str
    centro_poblado_id: int | None