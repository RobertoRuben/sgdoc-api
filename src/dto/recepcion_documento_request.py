from pydantic import BaseModel, field_validator, Field

class RecepcionDocumentoRequest(BaseModel):
    documento_id: int = Field(..., description="El id del documento es obligatorio")
    usuario_id: int = Field(..., description="El id del usuario es obligatorio")


    @field_validator("documento_id")
    def documento_id_getter_than_zero(cls, v):
        if v < 1:
            raise ValueError("El id del documento debe ser mayor a cero")
        return v

    @field_validator("usuario_id")
    def usuario_id_getter_than_zero(cls, v):
        if v < 1:
            raise ValueError("El id del usuario debe ser mayor a cero")
        return v

