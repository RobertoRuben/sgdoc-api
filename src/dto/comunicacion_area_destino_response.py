from pydantic import BaseModel

class ComunicacionAreaDestino(BaseModel):
    id: int
    nombre_area_destino: str