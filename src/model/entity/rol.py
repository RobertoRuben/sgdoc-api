from sqlmodel import SQLModel, Field, Column, Text

class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    id: int | None = Field(default=None, primary_key=True)
    nombre_rol: str = Field(sa_column=Column(Text, unique=True))