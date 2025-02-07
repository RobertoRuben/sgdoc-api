from pydantic import BaseModel

class RolReponseDTO(BaseModel):
    id: int
    nombre_rol: str

