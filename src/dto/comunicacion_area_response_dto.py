from pydantic import BaseModel

class ComunicacionAreaResponseDTO(BaseModel):
    id: int
    area_origen_nombre: str
    area_destino_nombre: str


class ComunicacionDestinoResponseDTO(BaseModel):
    area_destino_id: int
    nombre_area_destino: str