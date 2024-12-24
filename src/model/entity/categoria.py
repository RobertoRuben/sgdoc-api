from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity.documento import Documento

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    id: int | None = Field(default=None, primary_key=True)
    nombre_categoria: str = Field(sa_column=Column(Text, unique=True))

    documentos: list["Documento"] = Relationship(back_populates="categoria")

