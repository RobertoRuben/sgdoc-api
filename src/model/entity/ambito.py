from sqlmodel import SQLModel, Field, Column, Text

class Ambito(SQLModel, table = True):
    __tablename__ = "ambitos"
    id: int | None = Field(default = None, primary_key = True)
    nombre_ambito: str = Field(sa_column=Column(Text, unique=True))

