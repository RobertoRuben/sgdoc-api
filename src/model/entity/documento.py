from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP, Text

if TYPE_CHECKING:
    from src.model.entity import Remitente, Categoria, Ambito, Caserio, CentroPoblado, Derivacion, EstadoDocumento

class Documento(SQLModel, table=True):
    __tablename__ = "documentos"
    id: int | None = Field(default=None, primary_key=True)
    documento_bytes: bytes
    fecha_ingreso: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    folios: int = Field(ge=1)
    nombre: str = Field(sa_column=Column(Text, unique=True))
    asunto: str = Field(sa_column=Column(Text))
    remitente_id: int = Field(foreign_key="remitentes.id")
    categoria_id: int = Field(foreign_key="categorias.id")
    ambito_id: int = Field(foreign_key="ambitos.id")
    caserio_id: int | None = Field(default=None, foreign_key="caserios.id")
    centro_poblado_id: int | None = Field(default=None, foreign_key="centros_poblados.id")

    remitente: Optional[Remitente] = Relationship(back_populates="documentos")

    categoria: Optional[Categoria] = Relationship(back_populates="documentos")

    ambito: Optional[Ambito] = Relationship(back_populates="documentos")

    caserio: Optional[Caserio] = Relationship(back_populates="documentos")

    centro_poblado: Optional[CentroPoblado] = Relationship(back_populates="documentos")

    derivaciones: List["Derivacion"] = Relationship(back_populates="documento", cascade_delete=True)

    estados_documento: List["EstadoDocumento"] = Relationship(back_populates="documento", cascade_delete=True)

