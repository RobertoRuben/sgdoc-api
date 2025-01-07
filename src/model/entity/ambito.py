from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity.documento import Documento

class Ambito(SQLModel, table = True):
    __tablename__ = "ambitos"
    id: int | None = Field(default = None, primary_key = True)
    nombre_ambito: str = Field(sa_column=Column(Text, unique=True))

    documentos: List["Documento"] = Relationship(back_populates="ambito")

