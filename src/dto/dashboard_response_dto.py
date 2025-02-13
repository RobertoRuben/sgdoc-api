from typing import List, Dict, Any
from pydantic import BaseModel

class IngresosPorAmbitoResponseDTO(BaseModel):
    ambito: str
    total: int | None = None


class IngresosPorCaserioResponseDTO(BaseModel):
    caserio: str
    total_documentos: int | None = None


class IngresosPorCentroPobladoResponseDTO(BaseModel):
    mes: str
    centros: List[Dict[str, Any]] | None = None


class TotalIngresosResponseDTO(BaseModel):
    total_documentos: int | None = None


class PromedioIngresosResponseDTO(BaseModel):
    promedio_ingresos: float | None = None


class TopIngresosResponseDTO(BaseModel):
    caserio: str
    total_documentos: int | None = None