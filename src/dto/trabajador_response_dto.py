from pydantic import BaseModel

class TrabajadorResponseDTO(BaseModel):
    id: int
    dni: int | None = None
    nombres: str
    apellido_paterno: str | None = None
    apellido_materno: str | None = None
    genero: str | None = None
    area_id: int | None = None