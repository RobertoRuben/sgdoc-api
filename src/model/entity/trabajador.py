from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Column, Text, Relationship
from src.model.enum import GeneroEnum

if TYPE_CHECKING:
    from src.model.entity import Usuario, Area

class Trabajador(SQLModel, table=True):
    __tablename__ = "trabajadores"
    id: int | None = Field(default=None, primary_key=True)
    dni: int = Field(ge=10000000, le=99999999, unique=True)
    nombres: str = Field(sa_column=Column(Text, index= True))
    apellido_paterno: str = Field(sa_column=Column(Text, index=True))
    apellido_materno: str = Field(sa_column=Column(Text))
    genero: GeneroEnum
    area_id: int = Field(foreign_key="areas.id", index=True)

    area: Optional[Area] = Relationship(back_populates="trabajadores")

    usuarios: List["Usuario"] = Relationship(back_populates="trabajador")




