from sqlmodel import SQLModel, Field, Column, Text

class Area(SQLModel, table=True):
    __tablename__ = "areas"
    id: int | None = Field(default=None, primary_key=True)
    nombre_area: str = Field(sa_column=Column(Text, unique=True))