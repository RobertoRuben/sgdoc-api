from pydantic import BaseModel, Field, field_validator

class AmbitoRequest(BaseModel):
    nombre_ambito: str = Field(..., description="El nombre del ambito del documento es obligatorio")

    @field_validator("nombre_ambito")
    @classmethod
    def nombre_ambito_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del ambito del documento no debe quedar en blanco")
        return v

    @field_validator("nombre_ambito")
    @classmethod
    def nombre_ambito_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del ambito del documento no debe ser un número")
        return v