from sqlmodel import SQLModel, Field, Column, Text, Relationship
from src.model.enum.genero_enum import GeneroEnum
from src.model.entity.area import Area

class Trabajador(SQLModel, table=True):
    __tablename__ = "trabajadores"
    id: int | None = Field(default=None, primary_key=True)
    dni: int = Field(ge=10000000, le=99999999, unique=True)
    nombres: str = Field(sa_column=Column(Text))
    apellido_paterno: str = Field(sa_column=Column(Text))
    apellido_materno: str = Field(sa_column=Column(Text))
    genero: GeneroEnum

    area_id: int = Field(foreign_key="areas.id")
    area: Area | None = Relationship(back_populates="trabajadores")




