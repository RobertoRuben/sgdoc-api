from pydantic import BaseModel

class RolReponse(BaseModel):
    id: int
    nombre_rol: str

