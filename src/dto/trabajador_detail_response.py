from pydantic import BaseModel
class TrabajadorDetailResponse(BaseModel):
    id: int
    dni: int
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    genero: str
    nombre_area: str