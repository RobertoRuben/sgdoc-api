from pydantic import BaseModel

class AreaResponseDTO(BaseModel):
    id: int
    nombre_area: str