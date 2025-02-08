from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity import CentroPoblado, Documento

class Caserio(SQLModel, table=True):
    __tablename__ = "caserios"
    id: int | None = Field(default=None, primary_key=True)
    nombre_caserio: str = Field(sa_column=Column(Text, unique=True))
    centro_poblado_id: int | None = Field(default= None, foreign_key="centros_poblados.id", index=True)

    centro_poblado: Optional[CentroPoblado] = Relationship(back_populates="caserios")

    documentos: List["Documento"] = Relationship(back_populates="caserio")

