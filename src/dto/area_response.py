from pydantic import BaseModel

class AreaResponse(BaseModel):
    id: int
    nombre_area: str