from sqlmodel import SQLModel, Field, Column, Text

class CentroPoblado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre_centro_poblado: str = Field(sa_column=Column(Text, unique=True))