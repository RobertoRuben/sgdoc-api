from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

class ComunicacionArea(SQLModel, table=True):
    __tablename__ = "comunicacion_areas"
    __table_args__ = (
        UniqueConstraint("area_origen_id", "area_destino_id", name="unique_area_comunicacion"),
    )

    id: int | None = Field(default=None, primary_key=True)
    area_origen_id: int = Field(foreign_key="areas.id")
    area_destino_id: int = Field(foreign_key="areas.id")

    area_origen: "Area" = Relationship(
        back_populates="comunicaciones_origen",
        sa_relationship_kwargs={
            "primaryjoin": "and_(ComunicacionArea.area_origen_id == Area.id)",
            "overlaps": "comunicaciones_destino"
        }
    )
    area_destino: "Area" = Relationship(
        back_populates="comunicaciones_destino",
        sa_relationship_kwargs={
            "primaryjoin": "and_(ComunicacionArea.area_destino_id == Area.id)",
            "overlaps": "comunicaciones_origen"
        }
    )