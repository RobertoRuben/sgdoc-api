from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity import ComunicacionArea, Derivacion, Trabajador

class Area(SQLModel, table=True):
    __tablename__ = "areas"
    id: int | None = Field(default=None, primary_key=True)
    nombre_area: str = Field(sa_column=Column(Text, unique=True))

    comunicaciones_origen: List["ComunicacionArea"] = Relationship(
        back_populates="area_origen",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Area.id == ComunicacionArea.area_origen_id)",
            "overlaps": "comunicaciones_destino"
        }
    )

    comunicaciones_destino: List["ComunicacionArea"] = Relationship(
        back_populates="area_destino",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Area.id == ComunicacionArea.area_destino_id)",
            "overlaps": "comunicaciones_origen"
        }
    )

    derivaciones_origen: List["Derivacion"] = Relationship(
        back_populates="area_origen",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Area.id == Derivacion.area_origen_id)",
            "overlaps": "derivaciones_destino"
        }
    )

    derivaciones_destino: List["Derivacion"] = Relationship(
        back_populates="area_destino",
        sa_relationship_kwargs={
            "primaryjoin": "and_(Area.id == Derivacion.area_destino_id)",
            "overlaps": "derivaciones_origen"
        }
    )

    trabajadores: List["Trabajador"] = Relationship(back_populates="area")