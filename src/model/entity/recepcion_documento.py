from typing import TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Text, Relationship, TIMESTAMP
from src.model.entity.documento import Documento
from src.model.entity.usuario import Usuario

if TYPE_CHECKING:
    from src.model.entity.documento import Documento
    from src.model.entity.usuario import Usuario

class RecepcionDocumento(SQLModel, table=True):
    __tablename__ = "recepcion_documentos"
    id: int | None = Field(default=None, primary_key=True)
    fecha_recepcion: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))

    documento_id: int = Field(foreign_key="documentos.id")
    documento: Documento | None = Relationship(back_populates="recepcion_documentos")

    usuario_id: int = Field(foreign_key="usuarios.id")
    usuario: Usuario | None = Relationship(back_populates="recepcion_documentos")


