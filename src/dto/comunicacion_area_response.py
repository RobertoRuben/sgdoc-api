from pydantic import BaseModel

class ComunicacionAreaResponse(BaseModel):
    id: int
    area_origen_nombre: str
    area_destino_nombre: str

