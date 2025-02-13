from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Text, TIMESTAMP, Relationship
from src.model.enum import EstadoDerivacionEnum

if TYPE_CHECKING:
    from src.model.entity import Derivacion

class DetalleDerivacion(SQLModel, table=True):
    __tablename__ = "detalles_derivaciones"
    id: int | None = Field(default=None, primary_key=True)
    estado: EstadoDerivacionEnum
    comentario: str = Field(sa_column=Column(Text))
    fecha: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    recepcionada: bool | None = Field(default=False)
    usuario_id: int | None
    derivacion_id: int = Field(foreign_key="derivaciones.id", ondelete="CASCADE")

    derivacion: Optional["Derivacion"] = Relationship(back_populates="detalles_derivacion")