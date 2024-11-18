from pydantic import BaseModel, Field, field_validator

class CaserioRequest(BaseModel):
    nombre_caserio: str = Field(..., description="El nombre del caserio es obligatorio")
    centro_poblado_id: int | None = Field(None, description="El id del centro poblado es opcional")

    @field_validator("nombre_caserio")
    @classmethod
    def nombre_caserio_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del caserio no puede estar vacio")
        return v


    @field_validator("nombre_caserio")
    @classmethod
    def nombre_caserio_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del caserio no puede ser numerico")
        return v

    @field_validator("centro_poblado_id")
    @classmethod
    def centro_poblado_id_is_not_negative(cls, v):
        if v < 0:
            raise ValueError("El id del centro poblado no puede ser negativo")
        return v

    @field_validator("centro_poblado_id")
    @classmethod
    def centro_poblado_is_not_str(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del centro poblado no puede ser una cadena de texto")
        return v