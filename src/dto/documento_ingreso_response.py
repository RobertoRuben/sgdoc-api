from pydantic import BaseModel
from datetime import datetime

class DocumentoIngresoResponse(BaseModel):
    id: int
    nombre_documento: str
    dni_remitente: int
    ambito: str
    categoria: str
    caserio: str
    centro_poblado: str
    fecha_ingreso: datetime


