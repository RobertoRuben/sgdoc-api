from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Text, Relationship
from src.model.entity.centro_poblado import CentroPoblado

if TYPE_CHECKING:
    from src.model.entity.centro_poblado import CentroPoblado
    from src.model.entity.documento import Documento

class Caserio(SQLModel, table=True):
    __tablename__ = "caserios"
    id: int | None = Field(default=None, primary_key=True)
    nombre_caserio: str = Field(sa_column=Column(Text, unique=True))

    centro_poblado_id: int | None = Field(default= None, foreign_key="centros_poblados.id", index=True)

    centro_poblado: CentroPoblado | None = Relationship(back_populates="caserios")

    documentos: list["Documento"] = Relationship(back_populates="caserio")

