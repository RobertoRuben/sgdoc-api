from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP

if TYPE_CHECKING:
    from src.model.entity import Usuario, Area, Documento, DetalleDerivacion

class Derivacion(SQLModel, table=True):
    __tablename__ = "derivaciones"
    id: int | None = Field(default=None, primary_key=True)
    fecha: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    usuario_id: int | None = Field(default=None, foreign_key="usuarios.id")
    area_origen_id: int = Field(foreign_key="areas.id")
    area_destino_id: int = Field(foreign_key="areas.id")
    documento_id: int = Field(foreign_key="documentos.id", ondelete="CASCADE")

    usuario: Optional["Usuario"] = Relationship(back_populates="derivaciones")

    area_origen: Optional["Area"] = Relationship(
        back_populates="derivaciones_origen",
        sa_relationship_kwargs={"foreign_keys": "Derivacion.area_origen_id"}
    )

    area_destino: Optional["Area"] = Relationship(
        back_populates="derivaciones_destino",
        sa_relationship_kwargs={"foreign_keys": "Derivacion.area_destino_id"}
    )

    documento: Optional["Documento"] = Relationship(back_populates="derivaciones")

    detalles_derivacion: List["DetalleDerivacion"] = Relationship(back_populates="derivacion", cascade_delete=True)
