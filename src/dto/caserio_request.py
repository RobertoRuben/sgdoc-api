from pydantic import BaseModel, Field, field_validator

class CaserioRequest(BaseModel):
    nombre_caserio: str = Field(..., description="El nombre del caserio es obligatorio")
    centro_poblado_id: int | None = Field(None, description="El id del centro poblado es opcional")

    @field_validator("nombre_caserio")
    def nombre_caserio_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del caserio no puede estar vacio")
        return v


    @field_validator("nombre_caserio")
    def nombre_caserio_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del caserio no puede ser numerico")
        return v

    @field_validator("nombre_caserio")
    def nombre_caserio_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError(
                "El nombre del caserio no debe contener caracteres especiales, excepto espacios")
        return v

    @field_validator("nombre_caserio")
    def nombre_caserio_not_contains_numbers(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("El nombre del caserio no debe contener números")
        return v

    @field_validator("centro_poblado_id")
    def centro_poblado_id_is_not_negative(cls, v):
        if v < 0:
            raise ValueError("El id del centro poblado no puede ser negativo")
        return v

    @field_validator("centro_poblado_id")
    def centro_poblado_is_not_str(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del centro poblado no puede ser una cadena de texto")
        return v