from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP
from datetime import datetime

if TYPE_CHECKING:
    from src.model.entity.area import Area
    from src.model.entity.documento import Documento

class Derivacion(SQLModel, table=True):
    __tablename__ = "derivaciones"
    id: int | None = Field(default=None, primary_key=True)
    fecha: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    area_origen_id: int = Field(foreign_key="areas.id")
    area_origen: Optional["Area"] = Relationship(back_populates="derivaciones_origen")

    area_destino_id: int = Field(foreign_key="areas.id")
    area_destino: Optional["Area"] = Relationship(back_populates="derivaciones_destino")

    documento_id: int = Field(foreign_key="documentos.id")
    documento: Optional["Documento"] = Relationship(back_populates="derivaciones")
