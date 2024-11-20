from pydantic import BaseModel

class ComunicacionDestinoResponse(BaseModel):
    area_destino_id: int
    nombre_area_destino: str