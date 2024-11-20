from pydantic import BaseModel, field_validator

class ComunicacionAreaRequest(BaseModel):
    area_origen_id: int
    area_destino_id: int

    @field_validator("area_origen_id")
    @classmethod
    def validate_area_origen_id(cls, v):
        if v < 1:
            raise ValueError("El id del area origen debe ser mayor a 0")
        return v


    @field_validator("area_origen_id")
    @classmethod
    def validate_area_origen_is_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del area origen no puede ser un string")
        return v


    @field_validator("area_destino_id")
    @classmethod
    def validate_area_origen_is_not_area_destino(cls, v, values):
        if v == values.get("area_destino_id"):
            raise ValueError("El area origen no puede ser igual al area destino")
        return v


    @field_validator("area_destino_id")
    @classmethod
    def validate_area_destino_id(cls, v):
        if v < 1:
            raise ValueError("El id del area destino debe ser mayor a 0")
        return v


    @field_validator("area_destino_id")
    @classmethod
    def validate_area_destino_is_not_string(cls, v):
        if isinstance(v, str):
            raise ValueError("El id del area destino no puede ser un string")
        return v


    @field_validator("area_destino_id")
    @classmethod
    def validate_area_destino_is_not_area_origen(cls, v, values):
        if v == values.get("area_origen_id"):
            raise ValueError("El area destino no puede ser igual al area origen")
        return v