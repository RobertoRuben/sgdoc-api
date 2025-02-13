from pydantic import BaseModel

class RemitenteResponseDTO(BaseModel):
    id: int
    dni: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    genero: str
