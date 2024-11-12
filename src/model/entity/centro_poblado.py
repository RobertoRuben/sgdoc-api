from sqlmodel import SQLModel, Field, Column, Text, Relationship

class CentroPoblado(SQLModel, table=True):
    __tablename__ = "centros_poblados"
    id: int | None = Field(default=None, primary_key=True)
    nombre_centro_poblado: str = Field(sa_column=Column(Text, unique=True))

    caserios: list["Caserio"] = Relationship(back_populates="centro_poblado")