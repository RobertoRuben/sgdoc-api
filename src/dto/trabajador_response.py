from pydantic import BaseModel

class TrabajadorResponse(BaseModel):
    id: int
    dni: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    genero: str
    area_id: int