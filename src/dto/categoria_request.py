from pydantic import BaseModel, Field, field_validator

class CategoriaRequest(BaseModel):
    nombre_categoria: str = Field(..., description="El nombre de la categoría del documento es obligatorio y no debe quedar en blanco")

    @field_validator("nombre_categoria")
    @classmethod
    def nombre_categoria_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre de la categoría del documento no debe quedar en blanco")
        return v