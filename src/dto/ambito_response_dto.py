from pydantic import BaseModel

class AmbitoResponseDTO(BaseModel):
    id : int
    nombre_ambito : str

