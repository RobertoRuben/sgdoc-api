from datetime import datetime
from sqlmodel import SQLModel, Field, Column, TIMESTAMP, Text

class Notificacion(SQLModel, table=True):
    __tablename__ = "notificaciones"

    id: int | None  = Field(default=None, primary_key=True)
    comentario: str = Field(sa_column=Column(Text))
    area_destino_id: int
    leido: bool | None = Field(default=False)
    fecha_creacion: datetime | None = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
