from pydantic import BaseModel, Field, field_validator

class CategoriaRequest(BaseModel):
    nombre_categoria: str = Field(..., description="El nombre de la categoría del documento es obligatorio y no debe quedar en blanco")

    @field_validator("nombre_categoria")
    def nombre_categoria_is_not_blank(cls, v):
        if v.strip() == "":
            raise ValueError("El nombre de la categoría del documento no debe quedar en blanco")
        return v


    @field_validator("nombre_categoria")
    def nombre_categoria_is_not_numeric(cls, v):
        if v.isnumeric():
            raise ValueError("El nombre de la categoría del documento no debe ser un número")
        return v


    @field_validator("nombre_categoria")
    def nombre_categoria_not_contains_special_characters(cls, v):
        if not all(char.isalnum() or char.isspace() for char in v):
            raise ValueError(
                "El nombre de la categoría del documento no debe contener caracteres especiales, excepto espacios")
        return v


    @field_validator("nombre_categoria")
    def nombre_categoria_not_contains_numbers(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("El nombre de la categoría del documento no debe contener números")
        return v
