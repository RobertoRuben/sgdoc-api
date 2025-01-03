from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, Column, TIMESTAMP, Text
from src.model.entity.remitente import Remitente
from src.model.entity.categoria import Categoria
from src.model.entity.ambito import Ambito
from src.model.entity.caserio import Caserio
from src.model.entity.centro_poblado import CentroPoblado
from datetime import datetime

if TYPE_CHECKING:
    from src.model.entity.remitente import Remitente
    from src.model.entity.categoria import Categoria
    from src.model.entity.ambito import Ambito
    from src.model.entity.caserio import Caserio
    from src.model.entity.centro_poblado import CentroPoblado

class Documento(SQLModel, table=True):
    __tablename__ = "documentos"
    id: int | None = Field(default=None, primary_key=True)
    documento_bytes: bytes
    fecha_ingreso: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    folios: int = Field(ge=1)
    nombre: str = Field(sa_column=Column(Text, unique=True))
    asunto: str = Field(sa_column=Column(Text))

    remitente_id: int = Field(foreign_key="remitentes.id")
    remitente: Remitente | None = Relationship(back_populates="documentos")

    categoria_id: int = Field(foreign_key="categorias.id")
    categoria: Categoria | None = Relationship(back_populates="documentos")

    ambito_id: int = Field(foreign_key="ambitos.id")
    ambito: Ambito | None = Relationship(back_populates="documentos")

    caserio_id: int | None = Field(default=None, foreign_key="caserios.id")
    caserio: Caserio | None = Relationship(back_populates="documentos")

    centro_poblado_id: int | None = Field(default=None, foreign_key="centros_poblados.id")
    centro_poblado: CentroPoblado | None = Relationship(back_populates="documentos")

    recepcion_documentos: list["RecepcionDocumento"] = Relationship(back_populates="documento")

    derivaciones: list["Derivacion"] = Relationship(back_populates="documento")

