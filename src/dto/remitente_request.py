from pydantic import BaseModel, Field, field_validator
from src.model.enum.genero_enum import GeneroEnum

class RemitenteRequest(BaseModel):
    dni: int = Field(..., ge=10000000, le=99999999, description="El DNI es obligatorio y debe tener 8 dígitos")
    nombres: str = Field(..., description="El nombre es obligatorio y no debe quedar en blanco")
    apellido_paterno: str = Field(..., description="El apellido paterno es obligatorio y no debe quedar en blanco")
    apellido_materno: str = Field(..., description="El apellido materno es obligatorio y no debe quedar en blanco")
    genero: GeneroEnum = Field(..., description="El género es obligatorio y debe ser Masculino o Femenino")

    @field_validator("nombres")
    @classmethod
    def nombres_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre no debe quedar en blanco")
        return v


    @field_validator("nombres")
    @classmethod
    def nombres_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre no debe ser un número")
        return v


    @field_validator("apellido_paterno")
    @classmethod
    def apellido_paterno_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El apellido paterno no debe quedar en blanco")
        return v


    @field_validator("apellido_paterno")
    @classmethod
    def apellido_paterno_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El apellido paterno no debe ser un número")
        return v


    @field_validator("apellido_materno")
    @classmethod
    def apeliido_materno_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El apellido materno no debe quedar en blanco")
        return v


    @field_validator("apellido_materno")
    @classmethod
    def apellido_materno_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El apellido materno no debe ser un número")
        return v
