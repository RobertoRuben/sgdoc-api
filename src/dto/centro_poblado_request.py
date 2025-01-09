from pydantic import BaseModel, field_validator, Field

class CentroPobladoRequest(BaseModel):
    nombre_centro_poblado: str = Field(..., description="El nombre del centro poblado es obligatorio")

    @field_validator("nombre_centro_poblado")
    def nombre_centro_poblado_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del centro poblado no debe quedar en blanco")
        return v


    @field_validator("nombre_centro_poblado")
    def nombre_centro_poblado_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del centro poblado no debe ser un número")
        return v

    @field_validator("nombre_centro_poblado")
    def nombre_centro_poblado_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError(
                "El nombre del centro poblado no debe contener caracteres especiales, excepto espacios")
        return v

    @field_validator("nombre_centro_poblado")
    def nombre_centro_poblado_not_contains_numbers(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("El nombre del centro poblado no debe contener números")
        return v