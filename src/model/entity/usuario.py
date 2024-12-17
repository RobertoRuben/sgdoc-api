from datetime import datetime
from src.model.entity.rol import Rol
from src.model.entity.trabajador import Trabajador
from sqlmodel import SQLModel, Relationship, Field, Column, Text, TIMESTAMP

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: int | None = Field(default=None, primary_key=True)
    nombre_usuario: str = Field(sa_column=Column(Text, unique=True, index=True))
    contrasena: str = Field(sa_column=Column(Text))
    fecha_creacion: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now))
    fecha_actualizacion: datetime = Field(sa_column=Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now))
    is_active: bool = Field(default=True)
    rol_id: int = Field(foreign_key="roles.id")
    trabajador_id: int = Field(foreign_key="trabajadores.id", unique=True)

    roles: Rol | None = Relationship(back_populates="usuarios")
    trabajador: Trabajador | None = Relationship(back_populates="usuarios")
