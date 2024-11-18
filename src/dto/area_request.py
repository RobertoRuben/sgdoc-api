from pydantic import BaseModel, Field, field_validator

class AreaRequest(BaseModel):
    nombre_area: str = Field(..., description="El nombre del área municipal es obligatorio")

    @field_validator("nombre_area")
    @classmethod
    def nombre_area_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre del área municipal no debe quedar en blanco")
        return v

    @field_validator("nombre_area")
    @classmethod
    def nombre_area_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre del área municipal no debe ser un número")
        return v