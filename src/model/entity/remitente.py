from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Column, Text, Relationship
from src.model.enum.genero_enum import GeneroEnum

if TYPE_CHECKING:
    from src.model.entity.documento import Documento

class Remitente(SQLModel, table=True):
    __tablename__ = "remitentes"
    id: int | None = Field(default=None, primary_key=True)
    dni: int = Field(ge=10000000, le=99999999, unique=True)
    nombres: str = Field(sa_column=Column(Text, index=True))
    apellido_paterno: str = Field(sa_column=Column(Text, index=True))
    apellido_materno: str = Field(sa_column=Column(Text))
    genero: GeneroEnum

    documentos: List["Documento"] = Relationship(back_populates="remitente")
