from sqlmodel import SQLModel, Field, Column, Text

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    id: int | None = Field(default=None, primary_key=True)
    nombre_categoria: str = Field(sa_column=Column(Text, unique=True))

