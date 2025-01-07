from pydantic import BaseModel, Field, field_validator
from src.model.enum.estado_derivacion_enum import EstadoDerivacionEnum

class DetalleDerivacionRequest(BaseModel):
    estado: EstadoDerivacionEnum
    comentario: str | None = Field(None, description="Comentario del detalle de derivación")
    usuario_recepcion_id: int | None = Field(None, description="Id del usuario que recibe la derivación")
    derivacion_id: int = Field(..., description="Id de la derivación a la que pertenece el detalle")


    @field_validator("estado")
    def validate_estado_final(cls, v, values):
        if v == EstadoDerivacionEnum.finalizada and not values.get("usuario_recepcion_id"):
            raise ValueError("El estado FINALIZADO requiere un usuario de recepción")
        return v

    @field_validator("estado")
    def estado_not_null(cls, v):
        if v is None:
            raise ValueError("El estado no puede ser nulo")
        return v

    @field_validator("comentario")
    def comentario_not_numeric(cls, v):
        if v and v.isnumeric():
            raise ValueError("El comentario no puede ser numérico")
        return v

    @field_validator("usuario_recepcion_id")
    def usuario_recepcion_id_not_negative(cls, v):
        if v and v < 0:
            raise ValueError("El id del usuario de recepción no puede ser negativo")
        return v

    @field_validator("derivacion_id")
    def derivacion_id_not_negative(cls, v):
        if v < 0:
            raise ValueError("El id de la derivación no puede ser negativo")
        return v

