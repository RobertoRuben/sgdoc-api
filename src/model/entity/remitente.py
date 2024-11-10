from sqlmodel import SQLModel, Field, Column, Text
from src.model.enum.genero_enum import GeneroEnum

class Remitente(SQLModel, table=True):
    __tablename__ = "remitentes"
    id: int | None = Field(default=None, primary_key=True)
    dni: int = Field(ge=10000000, le=99999999, unique=True)
    nombres: str = Field(sa_column=Column(Text))
    apellido_paterno: str = Field(sa_column=Column(Text))
    apellido_materno: str = Field(sa_column=Column(Text))
    genero: GeneroEnum
