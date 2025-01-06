from pydantic import BaseModel, Field, field_validator

class DerivacionRequest(BaseModel):
    area_origen_id: int = Field(..., description="Id del area destino")
    area_destino_id: int = Field(..., description="Id del area destino")
    documento_id: int = Field(..., description="Id del documento")

    @field_validator("area_origen_id")
    def check_area_origen(cls, v):
        if v < 1:
            raise ValueError("El id del area origen debe ser mayor a 0")
        return v

    @field_validator("area_destino_id")
    def check_area_destino(cls, v):
        if v < 1:
            raise ValueError("El id del area destino debe ser mayor a 0")
        return v

    @field_validator("documento_id")
    def check_documento(cls, v):
        if v < 1:
            raise ValueError("El id del documento debe ser mayor a 0")
        return v