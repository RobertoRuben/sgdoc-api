from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import  SQLModel, Field, Column, TIMESTAMP, Text, Relationship
from src.model.enum import EstadoDocumentoEnum

if TYPE_CHECKING:
    from src.model.entity import Documento

class EstadoDocumento(SQLModel, table=True):
    __tablename__ = "estados_documentos"
    id: int | None = Field(default=None, primary_key=True)
    estado: EstadoDocumentoEnum
    fecha: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    comentario: str | None = Field(sa_column=Column(Text))
    documento_id: int | None = Field(foreign_key="documentos.id", ondelete="CASCADE")

    documento: Optional["Documento"] = Relationship(back_populates="estados_documento")

