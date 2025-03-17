from pydantic import BaseModel, field_validator, model_validator

class ComunicacionAreaRequestDTO(BaseModel):
    area_origen_id: int
    area_destino_id: int

    @field_validator("area_origen_id", "area_destino_id")
    def validate_positive(cls, value):
        if value <= 0:
            raise ValueError("El ID del área debe ser un número positivo.")
        return value

    @model_validator(mode="after")
    def validate_areas_diferentes(cls, model):
        if model.area_origen_id == model.area_destino_id:
            raise ValueError("El área de origen y el área de destino deben ser diferentes.")
        return model
