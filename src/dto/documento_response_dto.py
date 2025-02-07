from datetime import datetime
from pydantic import BaseModel

class DocumentoResponseDTO(BaseModel):
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


class DocumentosNoConfirmadosResponseDTO(BaseModel):
    total_documentos_no_confirmados: int

class DocumentosIngresadosResponseDTO(BaseModel):
    total_documentos: int


class TotalDocumentosDerivaodsResponseDTO(BaseModel):
    total_documentos_derivados: int


class TotalDocumentosNoDerivadosResponseDTO(BaseModel):
    total_documentos_no_derivados: int


class TotalDocumentosPorCaserioResponseDTO(BaseModel):
    nombre_caserio: str
    total_documentos_ingresados: int
