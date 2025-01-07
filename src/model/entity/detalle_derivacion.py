from typing import Optional

from sqlmodel import SQLModel, Field, Column, Text, TIMESTAMP, Relationship
from src.model.enum.estado_derivacion_enum import EstadoDerivacionEnum
from datetime import datetime

class DetalleDerivacion(SQLModel, table=True):
    __tablename__ = "detalles_derivaciones"
    id: int | None = Field(default=None, primary_key=True)
    estado: EstadoDerivacionEnum
    comentario: str = Field(sa_column=Column(Text))
    fecha: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    usuario_recepcion_id: int | None

    derivacion_id: int = Field(foreign_key="derivaciones.id")
    derivacion: Optional["Derivacion"] = Relationship(back_populates="detalles_derivacion")