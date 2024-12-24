from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, Text, Relationship

if TYPE_CHECKING:
    from src.model.entity.usuario import Usuario


class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    id: int | None = Field(default=None, primary_key=True)
    nombre_rol: str = Field(sa_column=Column(Text, unique=True))

    usuarios: list["Usuario"] = Relationship(back_populates="roles")
