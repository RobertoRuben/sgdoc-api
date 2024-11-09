from pydantic import BaseModel

class RemitenteResponse(BaseModel):
    id: int
    dni: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    genero: str
