from pydantic import BaseModel, Field, field_validator

class RolRequest(BaseModel):
    nombre_rol: str = Field(..., description="Nombre del rol es obligatorio")

    @field_validator("nombre_rol")
    @classmethod
    def nombre_rol_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del rol no debe quedar en blanco")
        return v

    @field_validator("nombre_rol")
    @classmethod
    def nombre_rol_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del rol no debe ser un número")
        return v
