from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity.caserio import Caserio
    from src.model.entity.documento import Documento

class CentroPoblado(SQLModel, table=True):
    __tablename__ = "centros_poblados"
    id: int | None = Field(default=None, primary_key=True)
    nombre_centro_poblado: str = Field(sa_column=Column(Text, unique=True))

    caserios: List["Caserio"] = Relationship(back_populates="centro_poblado")

    documentos: List["Documento"] = Relationship(back_populates="centro_poblado")