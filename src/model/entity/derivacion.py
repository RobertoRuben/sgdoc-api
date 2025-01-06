from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP
from datetime import datetime

if TYPE_CHECKING:
    from src.model.entity.area import Area
    from src.model.entity.documento import Documento

class Derivacion(SQLModel, table=True):
    __tablename__ = "derivaciones"
    id: int | None = Field(default=None, primary_key=True)
    fecha: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))


    area_origen_id: int = Field(foreign_key="areas.id")
    area_origen: Optional["Area"] = Relationship(
        back_populates="derivaciones_origen",
        sa_relationship_kwargs={"foreign_keys": "Derivacion.area_origen_id"}
    )

    area_destino_id: int = Field(foreign_key="areas.id")
    area_destino: Optional["Area"] = Relationship(
        back_populates="derivaciones_destino",
        sa_relationship_kwargs={"foreign_keys": "Derivacion.area_destino_id"}
    )

    documento_id: int = Field(foreign_key="documentos.id")
    documento: Optional["Documento"] = Relationship(back_populates="derivaciones")
