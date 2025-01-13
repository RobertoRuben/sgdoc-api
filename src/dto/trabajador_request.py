from pydantic import BaseModel, Field, field_validator
from src.model.enum.genero_enum import GeneroEnum

class TrabajadorRequest(BaseModel):
    dni:int = Field(..., ge=10000000, le=99999999, description="El dni es obligatorio")
    nombres:str = Field(..., description="El nombre es obligatorio")
    apellido_paterno:str = Field(..., description="El apellido paterno es obligatorio")
    apellido_materno:str = Field(..., description="El apellido materno es obligatorio")
    genero: GeneroEnum = Field(..., description="El género es obligatorio")
    area_id: int = Field(..., description="El id del área es obligatorio")

    @field_validator("dni")
    def dni_is_not_negative(cls, v):
        if v < 0:
            raise ValueError("El dni no debe ser negativo")
        return v


    @field_validator("dni")
    def dni_is_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El dni no puede ser un string")
        return v


    @field_validator("nombres")
    def nombres_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre no debe quedar en blanco")
        return v

    @field_validator("nombres")
    def nombres_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre no debe ser un número")
        return v


    @field_validator("nombres")
    def nombres_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError("El nombre del trabajador no debe contener caracteres especiales, excepto espacios")
        return v


    @field_validator("apellido_paterno")
    def apellido_paterno_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El apellido paterno no debe quedar en blanco")
        return v


    @field_validator("apellido_paterno")
    def apellido_paterno_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El apellido paterno no debe ser un número")
        return v


    @field_validator("apellido_paterno")
    def apellido_paterno_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError("El apellido paterno del trabajador no debe contener caracteres especiales, excepto espacios")
        return v


    @field_validator("apellido_materno")
    def apellido_materno_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El apellido materno no debe quedar en blanco")
        return v


    @field_validator("apellido_materno")
    def apellido_materno_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El apellido materno no debe ser un número")
        return v


    @field_validator("apellido_materno")
    def apellido_materno_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError("El apellido materno del trabajador no debe contener caracteres especiales, excepto espacios")
        return v


    @field_validator("genero")
    def genero_is_not_blank(cls, v):
        if v == "":
            raise ValueError("El género no debe quedar en blanco")
        return v


    @field_validator("genero")
    def genero_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El género no debe ser un número")
        return v


    @field_validator("area_id")
    def area_id_is_not_blank(cls, v):
        if v < 0:
            raise ValueError("El id del área no debe ser un numero negativo")
        return v


    @field_validator("area_id")
    def area_id_is_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del área no puede ser un string")
        return v


    @field_validator("area_id")
    def area_id_is_not_zero(cls, v):
        if v == 0:
            raise ValueError("El id del área no puede ser 0")
        return v