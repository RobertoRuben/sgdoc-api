from pydantic import BaseModel, Field,field_validator
from src.model.enum.estado_documento_enum import EstadoDocumentoEnum

class EstadoDocumentoRequest(BaseModel):
    estado: EstadoDocumentoEnum
    comentario: str | None = Field(None, description="Comentario del estado del documento")
    documento_id: int = Field(..., description="Id del documento al que pertenece el estado")

    @field_validator("documento_id")
    def documento_id_is_positive(cls, v):
        if v <= 0:
            raise ValueError("El id del documento debe ser un número positivo")
        return v
