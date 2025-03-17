from pydantic import BaseModel

class ComunicacionAreaSimpleResponseDTO(BaseModel):
    id: int
    area_origen_id: int | None = None
    area_destino_id: int | None = None
    area_origen_nombre: str | None = None
    area_destino_nombre: str | None = None


class ComunicacionDestinoResponseDTO(BaseModel):
    area_destino_id: int
    nombre_area_destino: str


class ComunicacionAreaFindResponseDTO(BaseModel):
    id: int
    nombre_area_origen: str
    nombre_area_destino: str