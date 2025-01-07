from pydantic import BaseModel, Field, field_validator

class AmbitoRequest(BaseModel):
    nombre_ambito: str = Field(..., description="El nombre del ambito del documento es obligatorio")

    @field_validator("nombre_ambito")
    def nombre_ambito_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del ambito del documento no debe quedar en blanco")
        return v

    @field_validator("nombre_ambito")
    def nombre_ambito_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del ambito del documento no debe ser un número")
        return v

    @field_validator("nombre_ambito")
    def nombre_ambito_not_contains_special_characters(cls, v):
        if not v.isalnum():
            raise ValueError("El nombre del ambito del documento no debe contener caracteres especiales")
        return v

    @field_validator("nombre_ambito")
    def nombre_ambito_not_contains_numbers(cls, v):
        if not v.isalpha():
            raise ValueError("El nombre del ambito del documento no debe contener números")
        return v